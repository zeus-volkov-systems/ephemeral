"""Controls execution of dask distributed tasks in a test environment.
"""

def run_one(client, function, element):
    """Runs a function on a single element (can be a data element or a future).
    Returns a future representing the action.
    """
    element_future = client.scatter(element)
    return client.submit(function, element_future)

def run_many(client, function, elements):
    """Runs a function on many elements (can be a collection or a future).
    Returns a future representing the action.
    """
    return client.map(function, elements)

def get_result(future):
    """Blocks and waits for the result from a future. Should not be used
    for large datasets or outside a test environment (either use persist or
    use some pub/sub strategy).
    """
    return future.result()
