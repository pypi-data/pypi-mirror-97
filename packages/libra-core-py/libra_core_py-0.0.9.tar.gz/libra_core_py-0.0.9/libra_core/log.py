import logging
import logging.config
from .config import config
from .log_id import get_logid
from inspect import getframeinfo, stack
import traceback

__log_path = '.'
__logger = None
__module_name = None
__is_debug = False
__log_name = 'root'
__log_callback = None
_log_config = None


def get_module_name():
    return __module_name


def _get_file_path(root_path, module_name):
    return root_path + '/' + module_name + '.log'


def is_debug_enabled():
    return __is_debug


def set_log_callback(log_callback):
    global __log_callback
    __log_callback = log_callback


def _get_config(root_path='.', is_console=True, module_name='', split_error_log=False):
    global __is_debug, __log_name
    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{asctime} [{processName}-{threadName}] {message}',
                'style': '{',
            },
        },
        'handlers': {
            'info': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': _get_file_path(root_path, module_name),
                'encoding': 'utf8',
                'formatter': 'verbose',
                'when': 'midnight',
                'backupCount': int(config('logging.handler.backup_count'))
            }
        }
    }
    handlers = ['info']
    if split_error_log:
        config_dict['handlers']['error'] = {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': _get_file_path(root_path, module_name + '.error'),
            'encoding': 'utf8',
            'formatter': 'verbose'
        }
        handlers = ['error', 'info']
    config_dict['root'] = {
        'handlers': handlers,
        'level': 'INFO',
    }
    if is_console:
        config_dict['handlers'] = {
            'console': {
                'class': 'logging.StreamHandler',
            }
        }
        config_dict['root'] = {
            'handlers': ['console'],
            'level': 'INFO',
        }
    elif __is_debug:
        config_dict['root']['level'] = 'DEBUG'
    return config_dict


def log_init_config(root_path, module_name, is_debug=None, split_error_log=False):
    global __logger, __module_name, __is_debug, __split_error_log, _log_config
    if is_debug is None:
        try:
            __is_debug = (config('log', 'logging.level.com.apus', 'info') == 'debug')
        except Exception as ex:
            pass
    else:
        __is_debug = is_debug
    __module_name = module_name
    __split_error_log = split_error_log
    _log_config = _get_config(root_path, root_path == 'console', module_name, split_error_log)
    logging.config.dictConfig(_log_config)
    __logger = logging.getLogger(__log_name)
    if not __is_debug:
        logging.getLogger("pika").setLevel(logging.WARNING)


def global_log_config():
    global _log_config
    return _log_config


def __log_id():
    return get_logid()


def _build_log_prefix(level):
    return "[{}] {} {} - ".format(__log_id(), level, _build_file_part())


def _build_file_part():
    caller = getframeinfo(stack()[3][0])
    return "{}[{}:{}]".format(caller.filename, caller.function, caller.lineno)


def log_debug(msg):
    global __is_debug
    if not __is_debug:
        return
    global __logger
    if __logger is None:
        return
    __logger.debug(_build_log_prefix("DEBUG") + msg)
    _callback_log_message("DEBUG", msg)


def log_trace(msg):
    # TODO 内存结构保存
    log_debug(msg)


def log_info(msg):
    global __logger
    if __logger is None:
        return
    __logger.info(_build_log_prefix("INFO") + msg)
    _callback_log_message("INFO", msg)


def log_warn(msg):
    global __logger
    if __logger is None:
        return
    __logger.warn(_build_log_prefix("WARN") + msg)
    _callback_log_message("WARN", msg)


def log_error(msg):
    global __logger, __error_callback
    if __logger is None:
        return
    __logger.error(_build_log_prefix("ERROR") + msg)
    _callback_log_message("ERROR", msg)


def log_exception(ex, message=""):
    global __logger
    if __logger is None:
        return
    if message is None:
        message = ""
    if message:
        message += " "
    message = "{}{}".format(message, ex)
    msg = '%s%s' % (_build_log_prefix("ERROR"), message)
    __logger.exception(msg)
    message = "{}{}".format(message, traceback.format_exc())
    _callback_log_message("ERROR", message)


def _callback_log_message(log_level, msg):
    global __log_callback
    if __log_callback:
        try:
            __log_callback(log_level, msg)
        except Exception as ex:
            pass
