"""Contains methods related to manipulation of xarray datasets in a test
environment.
"""

def make_on_variable(dataframe, variable):
    """Returns a new dataset created on the specified variable of the dataframe.
    """
    return dataframe[variable]

def get_statistic_function(statistic):
    """Returns the appropriate function for the given statistic string.
    """
    statistic_dict = {}
    statistic_dict["max"] = get_max
    statistic_dict["min"] = get_min
    statistic_dict["mean"] = get_mean
    return statistic_dict[statistic]

def get_max(dataset):
    """Returns the maximum value for the specified dataset.
    """
    return dataset.max()

def get_min(dataset):
    """Returns the maximum value for the specified dataset.
    """
    return dataset.min()

def get_mean(dataset):
    """Returns the mean value for the specified dataset.
    """
    return dataset.mean()

def get_as_list(dataset):
    """Returns the dataset as a list. First converts to ndarray then python list.
    This is a utility function for testing, do not use in production environment.
    """
    return dataset.values.tolist()
