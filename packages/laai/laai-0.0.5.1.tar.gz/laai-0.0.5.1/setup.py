from setuptools import setup, find_packages

setup(
	name='laai',
	version='0.0.5.1',
	py_modules=['laai.main'],
	install_requires=['click', 'python-dotenv', 'docker', 'mlflow'],
	extras_require={
        "optuna":  ["optuna", "sklearn", "plotly", "kaleido"],
    },
    include_package_data=True,
	packages = find_packages(),
	entry_points='''
		[console_scripts]
		laai=laai.main:cli
	'''
)

