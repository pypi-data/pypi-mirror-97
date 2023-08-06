from spaceone.api.inventory.v1 import job_pb2, job_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Job(BaseAPI, job_pb2_grpc.JobServicer):

    pb2 = job_pb2
    pb2_grpc = job_pb2_grpc

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('JobService', metadata) as job_service:
            job_vos, total_count = job_service.list(params)
            return self.locator.get_info('JobsInfo', job_vos, total_count, minimal=self.get_minimal(params))

    def stat(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('JobService', metadata) as job_service:
            return self.locator.get_info('StatisticsInfo', job_service.stat(params))
