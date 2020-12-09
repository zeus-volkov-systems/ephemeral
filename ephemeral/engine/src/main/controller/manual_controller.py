"""
The manual controller provides manual passing of a job map through a system
argument for single machine deployment.
"""
from sys import argv
import ephemeral.engine.src.main.driver.job_driver as job_driver


def route_request(request, resource=None):
    """Used to route an incoming string to a job request.
    """
    if request == 'file':
        return job_driver.build_job_from_file(resource)
    elif request == 'map':
        return job_driver.build_job_from_map(resource)

def submit_job(job):
    """Used for submitting a job.
    """
    print("Submitting a job for execution.")
    return job_driver.submit_job(job)


if __name__ == '__main__':
    print("Running main controller.")
    try:
        REQUEST_TYPE = argv[1]
        RESOURCE = argv[2]
        route_request(REQUEST_TYPE, resource=RESOURCE)
    except ValueError:
        print("Could not process request.")
