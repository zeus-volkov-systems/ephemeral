"""Tests a job that splits input into separate maps to test outputting vectors
from tasks.
"""

import unittest
import ephemeral.engine.src.main.controller.manual_controller as mc
import ephemeral.engine.src.test.utils.file_utils as file_utils


class TestMultiLayerVectorReturn(unittest.TestCase):
    """
    Tests a job that produces vectors from task outputs twice and propagates
    these vectors to ultimately produce an output.
    This tests the behavior of splitting tasks based on data.
    """
    TEST_JOB = "{}/engine/resources/test/job/multi-layer-vector-example/multi-layer-vector-job.json"
    job_file = file_utils.replace_path_keyword(TEST_JOB)

    def test_vector_outputs(self):
        """Runs a test based on the input map that takes a pair of lists
        (one of seasons, one of parameters), runs two tasks to first split
         based on season and return a vector of season outputs, then
        for each of those splits again on parameter.
        This should produce 4*3 = 12 input sets. These sets are then all fed
        into a single task to combine these parameters to demonstrate
        the pipeline. This behavior is useful for submitting
        many permutations of behaviors in a single stereotyped way.
        """
        expected = set(['springtmax', 'springtmin', 'springprecip',
                        'summertmax', 'summertmin', 'summerprecip',
                        'wintertmax', 'wintertmin', 'winterprecip',
                        'autumntmax', 'autumntmin', 'autumnprecip'])
        print(expected)
        job = mc.route_request("file", self.job_file)
        job_output = mc.submit_job(job)[0]
        print(job_output)
        real_output = set([output['combined'] for output in job_output['data']])
        print(real_output)
        self.assertEqual(real_output, expected)


if __name__ == '__main__':
    unittest.main()
