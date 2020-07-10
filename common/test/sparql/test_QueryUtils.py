import unittest
from common.sparql.QueryUtils import QueryUtils
from pkg_resources import resource_filename, resource_string


class QueryUtilsTest(unittest.TestCase):
    obj = QueryUtils()

    def test_read_prefixes(self):
        prefixes_path = resource_filename("common.test.resources.sparql", "prefixes-input.ttl")
        self.obj.set_prefixes(prefixes_path)
        actual = self.obj.get_prefixes()
        expected = resource_string("common.test.resources.sparql", "prefixes-output.rq")
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
