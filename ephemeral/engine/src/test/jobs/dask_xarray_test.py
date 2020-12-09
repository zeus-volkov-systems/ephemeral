"""Tests a job that does some basic operations on a NetCDF file open as a dask distributed dataset.
"""

import unittest
import ephemeral.engine.src.main.controller.manual_controller as mc
import ephemeral.engine.src.test.utils.file_utils as file_utils


class TestExamplePipeline(unittest.TestCase):
    """
    Testing the job builder pipeline.
    """
    TEST_JOB = "{}/engine/resources/test/job/dask-xarray-example/dask-xarray-example-job.json"
    job_file = file_utils.replace_path_keyword(TEST_JOB)

    def test_pipeline(self):
        """Tests the pipeline.
        Builds a job using the dask-xarray-example-job map and executes the
        job. This job demonstrates opening an example NetCDF file using xArray,
        creating/connecting to a local dask distributed client, and using that
        client to perform operations on the xArray.
        """
        expected = {}
        expected['max-out'] = 63.261104583740234
        expected['min-out'] = -24.159502029418945
        expected['mean-out'] = 9.034284591674805
        job = mc.route_request("file", self.job_file)
        job_output = mc.submit_job(job)
        for output in job_output:
            self.assertEqual(round(output['data'][0]['value'],3), round(expected[output['name']],3))


if __name__ == '__main__':
    unittest.main()
