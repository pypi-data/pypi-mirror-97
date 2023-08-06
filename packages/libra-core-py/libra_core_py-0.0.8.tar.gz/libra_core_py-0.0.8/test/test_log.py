import sys
sys.path.append('.')
from libra_core.log import *


def test_log_info():
    log_init_config("/tmp", "spider")
    log_info("test log info")


def test_log_warn():
    log_init_config("/tmp", "spider")
    log_warn("test log warn")

def error_callback(message):
    print("xxxx:" + message)

def test_log_error():
    set_error_callback(error_callback)
    log_init_config("/tmp", "spider1", split_error_log=True)
    log_error("test log error")


def test_log_debug():
    log_init_config("/tmp", "spider")
    log_debug("test log debug")


def test_log_exception():
    log_init_config("/tmp", "spider")
    try:
        print(1 / 0)
    except Exception as ex:
        log_exception(ex, "print failed")

if __name__ == "__main__":
    test_log_info()
