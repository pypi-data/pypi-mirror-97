from sevenbridges.meta.fields import (
    StringField, DateTimeField, CompoundField, BooleanField
)
from sevenbridges.meta.resource import Resource
from sevenbridges.models.compound.jobs.job_docker import JobDocker
from sevenbridges.models.compound.jobs.job_instance import Instance
from sevenbridges.models.compound.jobs.job_log import Logs


class Job(Resource):
    """
    Job resource contains information for a single executed node
    in the analysis.
    """
    name = StringField(read_only=True)
    start_time = DateTimeField(read_only=True)
    end_time = DateTimeField(read_only=True)
    status = StringField(read_only=True)
    command_line = StringField(read_only=True)
    retried = BooleanField(read_only=True)
    instance = CompoundField(Instance, read_only=True)
    docker = CompoundField(JobDocker, read_only=True)
    logs = CompoundField(Logs, read_only=True)

    def __str__(self):
        return f'<Job: name={self.name}, status={self.status}>'
