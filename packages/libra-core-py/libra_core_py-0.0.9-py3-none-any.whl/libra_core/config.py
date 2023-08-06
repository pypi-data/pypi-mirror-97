from .local_config import init_local_config, local_config
from .apollo_config import init_apollo_config, appllo_config

__inited = False


def init_config(search_path=None, hot_load=False, setting_file_name=None):
    global __inited
    __inited = True
    init_local_config(search_path, setting_file_name)
    app_id = local_config('apollo', 'app.id')
    if not app_id:
        return
    cluster = local_config('apollo', 'cluster')
    server = local_config('apollo', 'server')
    init_apollo_config(app_id, cluster, server, hot_load)


def config(section=None, key=None, default_value=None):
    if not __inited:
        init_config()
    try:
        val = local_config(section, key, None)
        if val is not None:
            return val
    except Exception as ex:
        pass
    return appllo_config(section, key, default_value)
