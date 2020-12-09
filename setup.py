"""
Controls package build for the engine of ephemeral
"""
from setuptools import setup, find_packages

setup(
    name='ephemeral',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'netCDF4',
        'dask',
        'distributed',
        'xarray',
        'nose',
        'nose-exclude'
      ],
    version='1.0',
    description='The ephemeral workflow engine.',
    author='Zeus Volkov Systems',
    author_email='contact@zeusvolkovsystems.com',
    url='https://www.github.com/zeusvolkovsystems/ephemeral/',
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
