from spaceone.core.service import *
from spaceone.inventory.manager.cloud_service_type_manager import CloudServiceTypeManager
from spaceone.inventory.manager.collection_data_manager import CollectionDataManager
from spaceone.inventory.error import *

_KEYWORD_FILTER = ['cloud_service_type_id', 'name', 'provider', 'group', 'service_code']


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class CloudServiceTypeService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.cloud_svc_type_mgr: CloudServiceTypeManager = self.locator.get_manager('CloudServiceTypeManager')

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['name', 'provider', 'group', 'domain_id'])
    def create(self, params):
        """
        Args:
            params (dict): {
                    'name': 'str',
                    'group': 'str',
                    'provider': 'str',
                    'service_code': 'str',
                    'is_primary': 'bool',
                    'is_major': 'bool',
                    'resource_type': 'str',
                    'metadata': 'dict',
                    'labels': 'list,
                    'tags': 'list',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        provider = params.get('provider', self.transaction.get_meta('secret.provider'))

        # Temporary Code for Tag Migration
        tags = params.get('tags')

        if isinstance(tags, dict):
            change_tags = []
            for key, value in tags.items():
                change_tags.append({
                    'key': key,
                    'value': value
                })
            params['tags'] = change_tags

        if provider:
            params['provider'] = provider

        params['resource_type'] = params.get('resource_type', 'inventory.CloudService')

        params['ref_cloud_service_type'] = f'{params["domain_id"]}.{params["provider"]}.' \
                                           f'{params["group"]}.{params["name"]}'

        params = data_mgr.create_new_history(params, exclude_keys=['domain_id', 'ref_cloud_service_type'])

        return self.cloud_svc_type_mgr.create_cloud_service_type(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['cloud_service_type_id', 'domain_id'])
    def update(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'service_code': 'str',
                    'is_primary': 'bool',
                    'is_major': 'bool',
                    'resource_type': 'str',
                    'metadata': 'dict',
                    'labels': 'list',
                    'tags': 'list',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        provider = params.get('provider', self.transaction.get_meta('secret.provider'))
        domain_id = params['domain_id']

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                           domain_id)
        # Temporary Code for Tag Migration
        tags = params.get('tags')

        if isinstance(tags, dict):
            change_tags = []
            for key, value in tags.items():
                change_tags.append({
                    'key': key,
                    'value': value
                })
            params['tags'] = change_tags

        if provider:
            params['provider'] = provider

        # if not cloud_svc_type_vo.ref_cloud_service_type:
        if True:
            params['ref_cloud_service_type'] = f'{domain_id}.' \
                                               f'{cloud_svc_type_vo.provider}.' \
                                               f'{cloud_svc_type_vo.group}.' \
                                               f'{cloud_svc_type_vo.name}'

        exclude_keys = ['cloud_service_type_id', 'domain_id', 'ref_cloud_service_type']
        params = data_mgr.merge_data_by_history(params, cloud_svc_type_vo.to_dict(), exclude_keys=exclude_keys)

        return self.cloud_svc_type_mgr.update_cloud_service_type_by_vo(params, cloud_svc_type_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['cloud_service_id', 'keys', 'domain_id'])
    def pin_data(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'keys': 'list',
                    'domain_id': 'str'
                }

        Returns:
            cloud_service_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                           params['domain_id'])

        params['collection_info'] = data_mgr.update_pinned_keys(params['keys'],
                                                                cloud_svc_type_vo.collection_info.to_dict())

        return self.cloud_svc_type_mgr.update_cloud_service_type_by_vo(params, cloud_svc_type_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['cloud_service_type_id', 'domain_id'])
    def delete(self, params):

        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'domain_id': 'str'
                }

        Returns:
            None

        """

        cloud_svc_type_vo = self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'],
                                                                           params['domain_id'])

        self.cloud_svc_type_mgr.delete_cloud_service_type_by_vo(cloud_svc_type_vo)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['cloud_service_type_id', 'domain_id'])
    def get(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'domain_id': 'str',
                    'only': 'list'
                }

        Returns:
            cloud_service_type_vo (object)

        """

        return self.cloud_svc_type_mgr.get_cloud_service_type(params['cloud_service_type_id'], params['domain_id'],
                                                              params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['cloud_service_type_id', 'name', 'provider', 'group', 'service_code', 'resource_type',
                          'is_primary', 'is_major', 'domain_id'])
    @change_tag_filter('tags')
    @append_keyword_filter(_KEYWORD_FILTER)
    def list(self, params):
        """
        Args:
            params (dict): {
                    'cloud_service_type_id': 'str',
                    'name': 'str',
                    'group': 'str',
                    'provider': 'str',
                    'service_code': 'str',
                    'resource_type': 'str',
                    'is_primary': 'str',
                    'is_major': 'str',
                    'domain_id': 'str',
                    'query': 'dict (spaceone.api.core.v1.Query)'
                }

        Returns:
            results (list)
            total_count (int)

        """

        return self.cloud_svc_type_mgr.list_cloud_service_types(params.get('query', {}))

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @change_tag_filter('tags')
    @append_keyword_filter(_KEYWORD_FILTER)
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get('query', {})
        return self.cloud_svc_type_mgr.stat_cloud_service_types(query)
