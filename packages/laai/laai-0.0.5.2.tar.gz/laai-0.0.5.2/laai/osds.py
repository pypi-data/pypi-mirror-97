import math
import fsspec
import tempfile
import warnings

import pandas as pd
import torch as pt
from torch.utils.data import IterableDataset

class TensorIterable(IterableDataset):
    def __init__(self, osds, dtype = pt.float32, max_iter = None):
        self.iter = iter(osds)
        self.dtype = dtype
        self.max_iter = max_iter

    def __iter__(self):        
        val = next(self.iter)
        while val is not None:
            try:
                yield pt.tensor(val.values.astype(float)).to(dtype = self.dtype)
                val = next(self.iter)
            except ValueError as err:
                raise ValueError(f"Failed data type conversion, use ObjectStorageDataset(header='infer') if the dataset has a header:  {err}")

    def __len__(self):
        if self.max_iter is None:
            return None
        else:
            return self.max_iter

def make_metadata_df(glob = None, df = None):    
    assert glob is not None or df is not None, "Either glob or df must be specified"
    df = pd.read_csv(glob) if glob else df
    assert set(df.columns) == set(['_partitionId', 'count']), "The metadata source must include _partitionId and count columns"
    df = df.sort_values(by='_partitionId', ignore_index=True)
    df['end_idx'] = df['count'].cumsum()
    df['start_idx'] = df['end_idx'] - df['count']
    df = df[['_partitionId', 'start_idx', 'end_idx']]
    return df

def objs_to_metadata_df(objs):    
    rows = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for idx, obj in enumerate(objs):
            df = pd.read_csv(f"filecache::{obj}", header = None)
            rows.append({"_partitionId": idx, "count": len(df),})
    return pd.DataFrame(rows)

def df_read_spec(df, row_count, row_start_idx, row_end_idx):

    assert row_start_idx > -1 and row_start_idx < row_count, f"row_start_idx must be in the range({0, row_count}]"
    assert row_end_idx > -1 and row_end_idx < row_count, f"row_end_idx must be in the range({0, row_count}]"

    start_obj_idx = df[ (row_start_idx >= df['start_idx']) & (row_start_idx < df['end_idx']) ]['_partitionId'].item()
    #max is needed to handle the case when the row_end_idx matches the end row of a partition and the start row of a partition
    #if the row_end_idx matches 2 partitions, calling item results in ValueError: can only convert an array of size 1 to a Python scalar
    end_obj_idx_res = df[ (row_end_idx >= df['start_idx']) & (row_end_idx <= df['end_idx']) ]['_partitionId'].max()    
    end_obj_idx = end_obj_idx_res if isinstance(end_obj_idx_res, int) else end_obj_idx_res.item()
    if row_end_idx > row_start_idx:
        
        df_spec = df.iloc[start_obj_idx : end_obj_idx + 1]
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df_spec.loc[:, 'skiprows'] = df_spec['start_idx'].apply(lambda i: max(0, row_start_idx - i))
            df_spec.loc[:, 'numrows'] = df_spec['end_idx'].apply(lambda i: min(i, row_end_idx)) - (df_spec['start_idx'] + df_spec['skiprows'])
            
        df_values = df_spec[['skiprows', 'numrows', 'uri']].values
    
    #handle the wrap-around case
    #when the shard consists
    #of a tail of a dataset
    #followed by the dataset head
    else:

        head_df = df.iloc[start_obj_idx : ]
        tail_df = df.iloc[ : end_obj_idx + 1] #if end_obj_idx > start_obj_idx else None
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            head_df.loc[:, 'skiprows'] = head_df['start_idx'].apply(lambda i: max(0, row_start_idx - i))
            head_df.loc[:, 'numrows'] = head_df['end_idx'] - (head_df['start_idx'] + head_df['skiprows'])

            if tail_df is not None:
                tail_df.loc[:, 'skiprows'] = 0
                tail_df.loc[:, 'numrows'] = tail_df['end_idx'].apply(lambda i: min(i, row_end_idx)) - tail_df['start_idx']

        df_values = pd.concat([head_df, tail_df], ignore_index = True)[['skiprows', 'numrows', 'uri']].values
        
    return [ (skiprows, numrows, uri) for (skiprows, numrows, uri) in df_values ]

class ObjectStorageDataset():        
    def __init__(self, 
                 glob, 
                 header = None, 
                 index_metadata = None,
                 metadata_glob = None, 
                 make_metadata_df_fn = make_metadata_df, 
                 objs_to_metadata_df_fn = objs_to_metadata_df,
                 worker = 0, 
                 replicas = 1, 
                 shard_size = 1, 
                 storage_options = None, 
                 cache_dir = None, 
                 iterations = None):
        
        assert glob, "glob must be specified"
        self.glob = glob
        
        self.header = header

        if index_metadata is None:
            if metadata_glob is None:
                index_metadata = True
            else:
                index_metadata = False
        else:
            assert isinstance(index_metadata, bool), "index_metadata must be set to True or False"

        assert make_metadata_df_fn, "make_metadata_df_fn must be specified"
        self.make_metadata_df_fn = make_metadata_df_fn

        if index_metadata is None \
                or index_metadata is True \
                or metadata_glob is not None:
            assert objs_to_metadata_df_fn, "objs_to_metadata_df_fn must be specified"
            self.objs_to_metadata_df_fn = objs_to_metadata_df_fn

        assert worker is not None or replicas is not None, "Both worker and replicas must be specified together along with shard_size"
        assert worker > -1 and worker < replicas, f"worker must be in the range [0, {replicas})"
        self.worker = worker
        self.replicas = replicas

        if self.replicas > 1:
            assert shard_size, "shard_size must be specified if replicas is greater than 1"
        self.shard_size = shard_size

        self.iterations = iterations if iterations else float('nan')

        # set the platform-specific temporary directory
        cache_dir = cache_dir if cache_dir else tempfile.gettempdir()

        # find out the protocol of the glob, e.g. s3, gs, hdfs, etc
        protocol, _ = fsspec.core.split_protocol(glob)
#         eager_load_batches = True if protocol in ('file') and eager_load_batches is None else eager_load_batches

        # use anonymous connection unless specified otherwise
        storage_options = storage_options if storage_options else {'anon': True}

        if protocol in ('http', 'https'):
            # setup a caching filesystem
            self.fs = fsspec.filesystem("filecache",
                                        target_protocol = protocol,
                                        target_options = storage_options,
                                        cache_storage = cache_dir)

        else:
            # setup a caching filesystem
            self.fs = fsspec.filesystem("filecache",
                                        target_protocol = protocol,
                                        target_options = storage_options,
                                        cache_storage = cache_dir)

        # get the object paths matching the glob
        if protocol in ('http', 'https'):
            protocol, uri = fsspec.core.split_protocol(glob)
            self.objs = [uri]
        else:
            self.objs = self.fs.glob(glob)

        if not isinstance(self.objs, list) or not len(self.objs):
            raise RuntimeWarning(f"Specified glob pattern {self.glob} failed to match any objects. Ensure that the permission setting are configured correctly using storage_options before trying again.")
            
        if index_metadata is None or index_metadata is True:
            objs = [f"{protocol}://{obj}" for obj in self.objs]
            self.metadata_df = make_metadata_df_fn(df = objs_to_metadata_df_fn(objs))
        else:            
            self.metadata_df = make_metadata_df_fn(glob = metadata_glob)
            
        self.metadata_df['uri'] = pd.Series(self.objs).apply(lambda s: f"{protocol}://{s}")
        
        self.obj_count = len(self.metadata_df)
        self.row_count = self.metadata_df.iloc[-1]['end_idx']

    def __iter__(self):

        shard_start_idx = self.worker * self.shard_size
        while self.iterations:
            try:
                num_rows, row_start_idx, row_end_idx = self.shard_size, shard_start_idx, shard_start_idx + self.shard_size
                
                #query rows
                row_start_idx = row_start_idx % self.row_count
                row_end_idx = row_end_idx % self.row_count

                if self.header is None:
                    src_df_list = [pd.read_csv(f"filecache::{uri}", header = None, nrows=nrows, skiprows=skiprows) for
                     (skiprows, nrows, uri) in df_read_spec(self.metadata_df, self.row_count, row_start_idx, row_end_idx)]
                elif self.header == 'infer' or self.header == 0:
                    src_df_list = []
                    for (skiprows, nrows, uri) in df_read_spec(self.metadata_df, self.row_count, row_start_idx, row_end_idx):
                        if (skiprows == 0):
                            src_df_list.append(pd.read_csv(f"filecache::{uri}", header=None, nrows = nrows, skiprows=skiprows + 1))
                        else:
                            src_df_list.append(pd.read_csv(f"filecache::{uri}", header=None, nrows=nrows, skiprows=skiprows))
                else:
                    raise ValueError(f"header attribute cannot be set to {self.header}")

                # map(lambda df: df.columns, src_df_list)
                # assert len(set(map(lambda df: df.shape[1], src_df_list))) == 1, f"Failed to process in the following fragment of the dataset {df_read_spec(self.metadata_df, self.row_count, row_start_idx, row_end_idx)} due to a change in the number of the columns."

                yield pd.concat(
                    objs = src_df_list,
                    copy = False
                )
                                
            finally:
                shard_start_idx += (self.replicas * self.shard_size)
                self.iterations -= 1
                