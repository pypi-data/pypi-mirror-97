from setuptools import setup
import os

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'pyrasgo', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='pyrasgo',
    version=version['__version__'],
    description=('Alpha version of the Rasgo Python interface.'),
    long_description='Alpha version of the Rasgo Python interface.',
    author='Patrick Dougherty',
    author_email='patrick@rasgoml.com',
    url='https://www.rasgoml.com/',
    license='MPL 2.0',
    packages=['pyrasgo',
              'pyrasgo.schemas',
              'pyrasgo.storage',
              'pyrasgo.utils',
              'pyrasgo.schemas.feature_set'],
    install_requires=[
        # Note these are duplicated in requirements.txt
        "requests==2.23.0",
        "pyarrow==0.17.0",
        "idna<2.10",
        "snowflake-connector-python>=2.3.8",
        "snowflake-connector-python[pandas]",
        "pydantic>=1.4",
        "pandas",
        "tqdm == 4.48.2",
        "uncompyle6==3.7.4",
        "pyyaml",
        "more-itertools==8.6.0"
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
)
