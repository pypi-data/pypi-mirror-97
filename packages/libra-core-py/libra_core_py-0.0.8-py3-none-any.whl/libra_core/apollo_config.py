from .apollo_client import ApolloClient

__apollo_client = None


def init_apollo_config(app_id, cluster_name, config_server_url, hot_load=False):
    global __apollo_client, __apollo_namespace
    if __apollo_client:
        return
    __apollo_client = ApolloClient(app_id=app_id, cluster=cluster_name, config_server_url=config_server_url)
    if hot_load:
        __apollo_client.start()


def appllo_config(namespace=None, key=None, default_value=None):
    if not key:
        key = namespace
        namespace = 'application'
    if not namespace:
        namespace = 'application'
    return __apollo_client.get_value(key, default_value, namespace)
