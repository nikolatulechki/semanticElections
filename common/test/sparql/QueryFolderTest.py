import unittest
from common.sparql.Executor import Executor
from common.sparql.QueryUtils import QueryUtils
from common.test.sparql.QueryTest import QueryTest
import os


class QueryFolderTest:

    def execute(self, query_folder, input_folder, expected_folder, executor):
        for filename in executor.list_files(query_folder, "ru"):
            query_name = os.path.join(query_folder, filename)
            input_file = os.path.join(input_folder, filename + ".ttl")
            output_file = os.path.join(expected_folder, filename + ".ttl")
            with open(query_name) as f:
                query = f.read()
                yield QueryTest(input_file, output_file, "ttl", query).execute_update_query()

