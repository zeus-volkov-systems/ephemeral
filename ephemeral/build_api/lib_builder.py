from ephemeral.build_api.lib_function import LibFunction
from ephemeral.build_api.job_builder import JobBuilder


class LibBuilder(object):

    def __init__(self):
        self.functions = []
        self.jobs = []

    def add_function(self, name, method):
        t = LibFunction(name, method)
        self.functions.append(t)
        return t

    def create_job(self, name):
        job = JobBuilder(name)
        self.jobs.append(job)
        return job