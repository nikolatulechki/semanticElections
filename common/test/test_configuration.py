import unittest
import os
import ConfigParser
from pkg_resources import resource_filename, resource_string
from common.configuration import ConfigurationBase


class ConfigurationTest(unittest.TestCase):
    config = '{ "DEFAULT": { "logging_level": "DEBUG" }, ' \
         '"sparql": { "endpoint_trr": "http://test-that-shit-up"} }'
    os.environ["CONFIG"] = config

    __config = ConfigurationBase()
    __config.set_config([resource_filename("common.test.resources", "config.ini")])
    __config.override_variables_from_environment()

    def test_logging_level(self):
        self.assertEqual(self.__config.get_config().get('DEFAULT', 'logging_level'), "DEBUG")

    def test_endpoint_trr(self):
        self.assertEqual(self.__config.get_config().get('sparql', 'endpoint_trr'), "http://test-that-shit-up")


if __name__ == '__main__':
    unittest.main()

