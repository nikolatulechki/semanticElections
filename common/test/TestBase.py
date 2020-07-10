import ConfigParser
from pkg_resources import resource_filename


class TestBase:
    __config = ConfigParser.ConfigParser()
    __config.read([resource_filename("common.test.resources", "config.ini")])

    def __init__(self):
        pass

    @staticmethod
    def get_file_content(path):
        with open(path, 'r') as f:
            return f.read()

    def get_config(self):
        return self.__config
