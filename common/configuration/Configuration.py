from pkg_resources import resource_filename
from common.configuration.ConfigurationBase import ConfigurationBase


class Configuration(ConfigurationBase):

    def __init__(self):
        super(ConfigurationBase, self).__init__()
        self.set_config(resource_filename("common.resources", "config.ini"))
        self.override_variables_from_environment()


if __name__ == '__main__':
    Configuration()
