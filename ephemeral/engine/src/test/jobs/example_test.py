"""Tests an example job.
"""

import unittest
import ephemeral.engine.src.main.controller.manual_controller as mc
import ephemeral.engine.src.test.utils.file_utils as file_utils


class TestExamplePipeline(unittest.TestCase):
    """
    Testing the job builder pipeline.
    """
    TEST_JOB = "{}/engine/resources/test/job/simple-example/simple-example-job.json"
    job_file = file_utils.replace_path_keyword(TEST_JOB)

    def test_pipeline(self):
        """Tests the pipeline.
        Builds a job using an example job map, validates all elements of the job,
        retrieves the proper example method for the job, and runs the job.
        """
        expected = [{"input": "We got: This is a test!this is our test string input"}]
        job = mc.route_request("file", self.job_file)
        job_output = mc.submit_job(job)
        self.assertEqual(job_output[0]["data"], expected)


if __name__ == '__main__':
    unittest.main()
