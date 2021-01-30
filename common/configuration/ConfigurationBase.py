import configparser
import os
import json
import logging


class ConfigurationBase(object):
    __config = configparser.ConfigParser()

    def __init__(self):
        pass

    def override_variables_from_environment(self):
        if "CONFIG" not in os.environ:
            return
        configs = json.loads(os.environ["CONFIG"])
        for section, section_dict in configs.iteritems():
            for key, value in section_dict.iteritems():
                self.__config.set(section, key, value)

    def set_config(self, config_path):
        self.__config.read(config_path)
        logging.getLogger().setLevel(self.__config.get('DEFAULT', 'logging_level'))

    def get_config(self):
        return self.__config

if __name__ == '__main__':
    pass

