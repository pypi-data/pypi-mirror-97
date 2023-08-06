import sys
sys.path.append('.')
from libra_core.config import *
from libra_core.utils import sleep


def test_local_config():
    init_local_config()
    print(local_config('apollo', 'server'))
    print(local_config('xxx', 'aaa', 'aaa'))
    print(local_config('log_path'))


def test_apollo_config():
    init_config()
    print(appllo_config("logging.level.com.apus"))
    print(appllo_config("log", "logging.level.com.apus"))
    print(appllo_config("channel_country_config"))


def test_config():
    init_config()
    print(config("log_path"))
    print(config("log", "logging.level.com.apus"))
    print(config("channel_country_config"))

def test_another_config():
    init_config(setting_file_name='settings.another.ini')
    print(config("property_a"))
    init_config()
    print(config("property_a"))


if __name__ == "__main__":
    test_apollo_config()
