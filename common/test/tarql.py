from common.tarql import Tarql
import  unittest
from common.test.TestBase import TestBase
from common.sparql.QueryUtils import QueryUtils
from pkg_resources import resource_filename, resource_string
import tempfile
from rdflib import Graph


def tarqls_compare(query_path, csv_path, expected_path, tarql_arguments):
    temp = tempfile.NamedTemporaryFile()
    Tarql(QueryUtils()).execute_query(query_path, csv_path, temp.name, tarql_arguments)
    return (sorted(list(Graph().parse(temp.name, format="ttl"))),
            sorted(list(Graph().parse(expected_path, format="ttl"))))


class TarqlTest(unittest.TestCase, TestBase):
    executor = Tarql(QueryUtils())

    def test_execute_query_pos(self):
        query_raw = resource_filename("common.test.resources.tarql", "query.tarql")
        csv = resource_filename("common.test.resources.tarql", "test.csv")
        expected_file = resource_filename("common.test.resources.tarql", "data.ttl")
        result = tarqls_compare(query_raw, csv, expected_file, "--encoding utf8 -d ;")
        self.assertEqual(result[0], result[1])

    def test_execute_query_neg(self):
        temp = tempfile.NamedTemporaryFile()
        query_raw = resource_filename("common.test.resources.tarql", "query.tarql")
        csv = resource_filename("common.test.resources.tarql", "test.csv")

        self.assertRaises(Exception, self.executor.execute_query, query_raw, csv, temp.name, "--encoding utf8 -dd ;")

    def test_execute_query_neg_no_qfile(self):
        temp = tempfile.NamedTemporaryFile()
        csv = resource_filename("common.test.resources.tarql", "test.csv")
        self.assertRaises(IOError,
                          self.executor.execute_query,
                          "dummy.file.query",
                          csv,
                          temp.name,
                          "--encoding utf8 -d ;")

    def test_execute_query_neg_no_csvfile(self):
        temp = tempfile.NamedTemporaryFile()
        query_raw = resource_filename("common.test.resources.tarql", "query.tarql")
        self.assertRaises(Exception,
                          self.executor.execute_query,
                          query_raw,
                          "dummy.file.query",
                          temp.name,
                          "--encoding utf8 -d ;")


if __name__ == '__main__':
    unittest.main()