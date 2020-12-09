"""Contains methods for manipulating dask distributed clients and connections
in a test environment.
"""
from dask.distributed import Client

def create_local_environment():
    """Establishes and returns a local connection.
    """
    return Client()
