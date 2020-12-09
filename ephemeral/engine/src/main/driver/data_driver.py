"""
Used to drive the processing of job datasources.
"""

def get_data(datasource):
    """Drives the collection and assembly of the initial data for a given job.
    """
    if datasource["source"] == "direct":
        return datasource["content"]
