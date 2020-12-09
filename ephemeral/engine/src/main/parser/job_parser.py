"""
A library containing methods used for parsing jobs between python
data structures and json.
"""
import logging
import ephemeral.engine.src.main.parser.base_parser as base_parser

logger = logging.getLogger(__name__)

def parse_job_from_file(job_map):
    """Parses a json string and returns a dictionary representing the job.
    """
    logger.info("Parsing a job map from a file.")
    job_dict = base_parser.parse_json_from_file(job_map)
    return job_dict
