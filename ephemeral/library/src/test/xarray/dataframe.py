"""Contains methods related to manipulation of xarray dataframes in a test
environment.
"""
import xarray

def make_from_netcdf(netcdf_source):
    """Creates and returns a new dataframe from a netcdf source.
    """
    return xarray.open_dataset(netcdf_source)
