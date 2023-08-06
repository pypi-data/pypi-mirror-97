import functools
from spaceone.api.core.v1 import tag_pb2
from spaceone.api.inventory.v1 import cloud_service_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.model.cloud_service_model import CloudService
from spaceone.inventory.info.region_info import RegionInfo
from spaceone.inventory.info.collection_info import CollectionInfo

__all__ = ['CloudServiceInfo', 'CloudServicesInfo']


def CloudServiceInfo(cloud_svc_vo: CloudService, minimal=False):
    info = {
        'cloud_service_id': cloud_svc_vo.cloud_service_id,
        'cloud_service_group': cloud_svc_vo.cloud_service_group,
        'cloud_service_type': cloud_svc_vo.cloud_service_type,
        'provider': cloud_svc_vo.provider,
        'reference': cloud_service_pb2.CloudServiceReference(
            **cloud_svc_vo.reference.to_dict()) if cloud_svc_vo.reference else None,
        'project_id': cloud_svc_vo.project_id,
        'region_code': cloud_svc_vo.region_code
    }

    if not minimal:
        info.update({
            'state': cloud_svc_vo.state,
            'data': change_struct_type(cloud_svc_vo.data),
            'metadata': change_struct_type(cloud_svc_vo.metadata),
            'tags': [tag_pb2.Tag(key=tag.key, value=tag.value) for tag in cloud_svc_vo.tags],
            'collection_info': CollectionInfo(cloud_svc_vo.collection_info.to_dict()),
            'domain_id': cloud_svc_vo.domain_id,
            'created_at': change_timestamp_type(cloud_svc_vo.created_at),
            'updated_at': change_timestamp_type(cloud_svc_vo.updated_at),
            'deleted_at': change_timestamp_type(cloud_svc_vo.deleted_at),
        })

    return cloud_service_pb2.CloudServiceInfo(**info)


def CloudServicesInfo(cloud_svc_vos, total_count, **kwargs):
    return cloud_service_pb2.CloudServicesInfo(results=list(
        map(functools.partial(CloudServiceInfo, **kwargs), cloud_svc_vos)), total_count=total_count)
