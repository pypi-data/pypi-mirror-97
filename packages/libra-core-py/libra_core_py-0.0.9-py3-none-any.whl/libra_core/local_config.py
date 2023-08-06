# coding: utf-8
import os
import sys
from configparser import ConfigParser

text_type = str


class UndefinedValueError(Exception):
    pass


class Undefined(object):
    """
    Class to represent undefined type.
    """
    pass


# Reference instance to represent undefined values
undefined = Undefined()


class Config(object):
    """
    Handle .env file format used by Foreman.
    """
    _BOOLEANS = {'1': True, 'yes': True, 'true': True, 'on': True,
                 '0': False, 'no': False, 'false': False, 'off': False, '': False}

    def __init__(self, repository):
        self.repository = repository

    def _cast_boolean(self, value):
        """
        Helper to convert config values to boolean as ConfigParser do.
        """
        value = str(value)
        if value.lower() not in self._BOOLEANS:
            raise ValueError('Not a boolean: %s' % value)

        return self._BOOLEANS[value.lower()]

    @staticmethod
    def _cast_do_nothing(value):
        return value

    def get(self, section, option=None, default=None, cast=undefined):
        """
        Return the value for option or default if defined.
        """
        if not option:
            option = section
            section = 'settings'

        value = self.repository.get(section, option, default)
        if isinstance(cast, Undefined):
            cast = self._cast_do_nothing
        elif cast is bool:
            cast = self._cast_boolean
        return cast(value)

    def __call__(self, *args, **kwargs):
        """
        Convenient shortcut to get.
        """
        return self.get(*args, **kwargs)


class RepositoryEmpty(object):
    def __init__(self, source=''):
        pass

    def __contains__(self, key):
        return False

    def __getitem__(self, key):
        return None


class RepositoryIni(RepositoryEmpty):
    """
    Retrieves option keys from .ini files.
    """
    SECTION = 'settings'

    def __init__(self, source):
        self.parser = ConfigParser()
        with open(source, encoding='utf-8') as file_:
            self.parser.read_file(file_)

    def get(self, section, key, default_value=None):
        if default_value is not None:
            try:
                return self.parser.get(section, key)
            except:
                return default_value
        return self.parser.get(section, key)


class AutoConfig(object):

    def __init__(self, setting_file_name, search_path=None):
        self.search_path = search_path
        self.config = None
        self.setting_file_name = setting_file_name

    def _find_file(self, path):
        filename = os.path.join(path, self.setting_file_name)
        if os.path.isfile(filename):
            return filename

        # search the parent
        parent = os.path.dirname(path)
        if parent and parent != os.path.sep:
            return self._find_file(parent)

        # reached root without finding any files.
        return ''

    def _load(self, path):
        # Avoid unintended permission errors
        try:
            filename = self._find_file(os.path.abspath(path))
        except Exception:
            filename = ''
        if filename:
            Repository = RepositoryIni
        else:
            Repository = RepositoryEmpty
        self.config = Config(Repository(filename))

    def _caller_path(self):
        # MAGIC! Get the caller's module path.
        frame = sys._getframe()
        path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
        return path

    def __build_env_key(self, *args):
        if len(args) == 1:
            return args[0].upper()
        if len(args) == 2:
            if not args[0]:
                return args[1].upper()
            return '{}_{}'.format(args[0].upper(), args[1].upper())
        return ''

    def _load_env(self, *args):
        key = self.__build_env_key(*args)
        return os.environ.get(key, None)

    def __call__(self, *args, **kwargs):
        if os.environ.get('IS_ENV', '0') == '1':
            value = self._load_env(*args)
            if value is not None:
                return value
        if not self.config:
            self._load(self.search_path or self._caller_path())
        return self.config(*args, **kwargs)


__local_config = None


def init_local_config(search_path=None, setting_file_name=None):
    global __local_config
    if not setting_file_name:
        setting_file_name = 'settings.ini'
    __local_config = AutoConfig(setting_file_name, search_path)


def local_config(section=None, key=None, default_value=None):
    global __local_config
    if not __local_config:
        init_local_config()
    return __local_config(section, key, default_value)
