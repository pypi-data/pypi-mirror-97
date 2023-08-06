import functools
import logging
from spaceone.api.core.v1 import tag_pb2
from spaceone.api.inventory.v1 import region_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.model.region_model import Region

__all__ = ['RegionInfo', 'RegionsInfo']

_LOGGER = logging.getLogger()


def RegionInfo(region_vo: Region, minimal=False):
    info = {
        'region_id': region_vo.region_id,
        'name': region_vo.name,
        'region_code': region_vo.region_code,
        'provider': region_vo.provider
    }

    if not minimal:
        info.update({
            'created_at': change_timestamp_type(region_vo.created_at),
            'updated_at': change_timestamp_type(region_vo.updated_at),
            'tags': [tag_pb2.Tag(key=tag.key, value=tag.value) for tag in region_vo.tags],
            'domain_id': region_vo.domain_id
        })

    return region_pb2.RegionInfo(**info)


def RegionsInfo(region_vos, total_count, **kwargs):
    return region_pb2.RegionsInfo(results=list(map(functools.partial(RegionInfo, **kwargs), region_vos)),
                                  total_count=total_count)
