from pyapollo.apollo_client import ApolloClient

__apollo_client = None
__apollo_namespace = None


def init_apollo_config(app_id, cluster_name, config_server_url, namespace):
    global __apollo_client, __apollo_namespace
    if __apollo_client:
        return
    __apollo_client = ApolloClient(app_id=app_id, cluster=cluster_name, config_server_url=config_server_url)
    __apollo_client.start()
    __apollo_namespace = namespace


def appllo_config(key, default_value=None):
    return __apollo_client.get_value(key, default_value, __apollo_namespace)
