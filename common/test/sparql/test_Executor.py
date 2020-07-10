import unittest
from common.sparql.Executor import Executor
from common.sparql.QueryUtils import QueryUtils
from pkg_resources import resource_filename, resource_string
from common.test.TestBase import TestBase
from common.test.sparql.QueryTest import QueryTest
from common.test.sparql.QueryFolderTest import QueryFolderTest


class ExecutorTest(unittest.TestCase, TestBase):
    qutils = QueryUtils()
    qutils.set_prefixes(resource_filename("common.test.resources.sparql", "prefixes-input.ttl"))
    executor = Executor(qutils)
    executor.query_utils.set_prefixes(resource_filename("common.test.resources.sparql", "prefixes-input.ttl"))

    def test_read_prefixes(self):
        query_raw = self.get_file_content(resource_filename("common.test.resources.sparql.execute", "query1.rq"))
        actual = self.executor.add_prefixes_to_query(query_raw, "")
        expected = self.get_file_content(resource_filename("common.test.resources.sparql.execute", "query1-with-prefixes"))
        self.assertEqual(actual, expected)

    def test_clean_graph_with_prefixes(self):
        actual = self.executor.add_prefixes_to_query(self.executor.get_clear_graph_template(), "")
        expected = self.get_file_content(resource_filename("common.test.resources.sparql.execute", "query1-clear"))
        self.assertEqual(actual, expected)

    def test_list_files(self):
        dir_name = resource_filename("common.test.resources.sparql", "execute")
        files = list(self.executor.list_files(dir_name, "rq"))
        self.assertEqual(["query1.rq", "query2.rq", "query3.rq"], files)

    def test_one_query_execution(self):
        query = resource_string("common.test.resources.sparql-update.query", "500-trr-organization-prefname.ru")
        input_ttl = resource_filename("common.test.resources.sparql-update.input", "500-trr-organization-prefname.ru.ttl")
        output_ttl = resource_filename("common.test.resources.sparql-update.output", "500-trr-organization-prefname.ru.ttl")
        result = QueryTest(input_ttl, output_ttl, "ttl", query).execute_update_query()
        self.assertEqual(result[0], result[1])

    def test_folder_query_execution(self):
        query = resource_filename("common.test.resources.sparql-update", "query")
        input_ttl = resource_filename("common.test.resources.sparql-update", "input")
        output_ttl = resource_filename("common.test.resources.sparql-update", "output")
        for x, y in QueryFolderTest().execute(query, input_ttl, output_ttl, self.executor):
            self.assertEqual(x, y)

    # Integration tests
    def it_execute_query_positive(self):
        query = "select * { ?s ?p ?o } limit 10"
        self.assertTrue(self.executor.execute_query(query, self.get_config().get("sparql", "endpoint_trr"))[0])

    def it_execute_query_negative(self):
        query = "select * { ?s ?p ?o } li"
        self.assertFalse(self.executor.execute_query(query, self.get_config().get("sparql", "endpoint_trr"))[0])


if __name__ == '__main__':
    unittest.main()
