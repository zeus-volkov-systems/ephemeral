"""
Library containing methods used for validating a job represented as a python
dictionary.
"""
from ephemeral.engine.src.main.validator import (
    datasource_validator as datasource_validator,
    task_validator as task_validator,
    workflow_validator as workflow_validator)
import ephemeral.engine.src.main.validator.base_validator as base_validator


def validate_job(job_map):
    """Validates an entire job and its contents against expected
    definition and contents.
    """
    if (validate_definition(job_map) and
            task_validator.validate_tasks(job_map["tasks"]) and
            datasource_validator.validate_datasource(job_map["datasource"]) and
            workflow_validator.validate_workflow(job_map["workflow"],
                                                 job_map["tasks"])):
        return True
    return False


def get_job_definition():
    """Returns the job definition as a python dictionary.
    """
    return base_validator.get_main_definition("job")


def validate_field_definition(definition, actual):
    """Validates a given top level job key against its definition.
    Returns a boolean of the validation.
    """
    if base_validator.validate_type(actual, definition["type"]):
        return True
    return False


def get_unique_job_id():
    """Returns a unique job id for the job.
    """
    return base_validator.get_unique_id(15)


def validate_definition(job_map):
    """Validates a job definition by validating keys.
    Returns a boolean representing an aggregate of job validation.
    """
    try:
        job_definition = get_job_definition()
        valid_list = [validate_field_definition(defn, job_map[defn["name"]])
                      for defn in job_definition["fields"]]
        valid = list(set(valid_list))
        if len(valid) == 1 and valid[0]:
            return True
        return False
    except KeyError:
        print("Key not found during job definition validation.")
        return False
