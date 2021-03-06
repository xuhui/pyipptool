import os

from future import standard_library
with standard_library.hooks():
    import configparser


def read_config(paths=()):
    config = {}
    fs_config = configparser.ConfigParser()
    fs_config.read(paths)
    config['cups_uri'] = fs_config.get('main', 'cups_uri')
    config['ipptool_path'] = fs_config.get('main', 'ipptool_path')
    try:
        config['login'] = fs_config.get('main', 'login')
    except configparser.NoOptionError:
        pass
    try:
        config['password'] = fs_config.get('main', 'password')
    except configparser.NoOptionError:
        pass
    try:
        config['graceful_shutdown_time'] = fs_config.getint(
            'main',
            'graceful_shutdown_time')
    except configparser.NoOptionError:
        config['graceful_shutdown_time'] = 2
    try:
        config['timeout'] = fs_config.getint('main', 'timeout')
    except configparser.NoOptionError:
        config['timeout'] = 10
    return config


class LazyConfig(dict):
    def __init__(self, paths):
        self.paths = paths
        self.loaded = False

    def __getitem__(self, key):
        if not self.loaded:
            self.update(read_config(self.paths))
            self.loaded = True
        return super(LazyConfig, self).__getitem__(key)


def get_config(paths=('/etc/opt/pyipptool/pyipptool.cfg',
                      os.path.join(os.path.expanduser('~'),
                                   '.pyipptool.cfg'))):
    return LazyConfig(paths)
