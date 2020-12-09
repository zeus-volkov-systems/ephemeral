"""
Used to drive the building and processing of jobs.
"""
import logging
import ephemeral.engine.src.main.parser.job_parser as job_parser
import ephemeral.engine.src.main.validator.job_validator as job_validator
import ephemeral.engine.src.main.processor.job_processor as job_processor
import ephemeral.engine.src.main.driver.task_driver as task_driver
import ephemeral.engine.src.main.driver.data_driver as data_driver

logger = logging.getLogger(__name__)


def build_job_from_file(job_map_path):
    """
    Cleans up a job path, filling out relative path keywords,
    and then submits the job json for processing.
    """
    job_map = job_parser.parse_job_from_file(job_map_path)
    return build_job_from_map(job_map)


def build_job_from_map(job_map):
    """Submits a job directly from a job map.
    """
    if "id" not in job_map:
        job_map["id"] = job_validator.get_unique_job_id()
    if job_validator.validate_job(job_map):
        job = {}
        job["tasks"] = task_driver.build_tasks(job_map)
        job["data"] = data_driver.get_data(job_map["datasource"])
        return job
    else:
        logger.error("Could not build the job.")
    return None


def submit_job(job):
    """Executes a submitted job.
    """
    tasks = job["tasks"]
    data = job["data"]
    task_map = task_driver.build_task_map(tasks)
    job_processor.run_job(tasks, task_map, data)
    return task_driver.get_output_tasks(tasks)
