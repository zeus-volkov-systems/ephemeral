"""Tests a job with multiple branches in the workflow..
"""

import unittest
import ephemeral.engine.src.main.controller.manual_controller as mc
import ephemeral.engine.src.test.utils.file_utils as file_utils


class TestBranchingPipeline(unittest.TestCase):
    """
    Tests a job that has a workflow which branches into separate processing
    and output paths.
    """
    TEST_JOB = "{}/engine/resources/test/job/branching-example/branching-example-job.json"
    job_file = file_utils.replace_path_keyword(TEST_JOB)

    def test_branching(self):
        """Tests the pipeline against a branching workflow. Compares the
        output coming from the job to the expected output.
        """
        expected = [2, 5, 3, 2, 5]
        print(self.job_file)
        job = mc.route_request("file", self.job_file)
        print(job)
        job_output = mc.submit_job(job)
        for output in job_output:
            if output["name"] == "short-output":
                self.assertEqual(output["data"][0]['lengths'], expected)


if __name__ == '__main__':
    unittest.main()
