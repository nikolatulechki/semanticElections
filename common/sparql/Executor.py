import glob, os
import requests
import logging
import json
from pkg_resources import resource_string
from common.sparql.QueryUtils import QueryUtils


class Executor:
    __clear_graph_template = "clear silent graph <{{graph}}>"

    def __init__(self, query_utils):
        self.query_utils = query_utils

    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        lgt = len(lst)
        for i in range(0, lgt, n):
            logging.info("BATCH {} - {} of {} ".format(i, i+n, lgt))
            yield lst[i:i + n]

    @staticmethod
    def list_files(path, file_type):
        saved_path = os.getcwd()
        os.chdir(path)
        try:
            for file_path in sorted(glob.glob("*." + file_type)):
                yield file_path
        finally:
            os.chdir(saved_path)

    def get_graph_size(self, graph, endpoint, query):
        if ":dropConnector" in query or \
                ":createConnector" in query or \
                "drop silent graph" in query or \
                "drop graph" in query or \
                ("http://www.ontotext.com/connectors/mongodb/instance#" in query
                 and ":service" in query):
            return 0
        count_query = "select (count(*) as ?cnt) where { graph <{{graph}}> { ?s ?p ?o } }"
        count_query_with_pref = self.add_prefixes_to_query(count_query, graph)
        response = self.handle_request(count_query_with_pref, endpoint.replace("/statements", ""), "validation")
        count = int(json.loads(response[1])["results"]["bindings"][0]["cnt"]["value"])
        if count == 0:
            raise Exception("No statements added for graph {}".format(graph))
        return count

    def execute_folder(self, path, file_type, endpoint):
        for query_file in self.list_files(path, file_type):
            absolute_path = os.path.join(path, query_file)
            with open(absolute_path, 'r') as myfile:
                data = myfile.read()
            clear_with_prefixes = self.add_prefixes_to_query(self.__clear_graph_template, query_file)
            query_with_prefixes = self.add_prefixes_to_query(data, query_file)
            self.handle_request(clear_with_prefixes, endpoint, absolute_path)
            self.handle_request(query_with_prefixes, endpoint, absolute_path)
            size = self.get_graph_size(graph=query_file, endpoint=endpoint, query=query_with_prefixes)
            if size > 0:
                self.add_graph_metadata(graph=query_file, endpoint=endpoint, triples=size)

    def execute_folder_values(self, path, file_type, endpoint):
        for query_file in self.list_files(path, file_type):
            absolute_path = os.path.join(path, query_file)
            values_absolute_path = os.path.join(path, query_file + '.values')
            with open(values_absolute_path, 'r') as myfile:
                data = myfile.read()
            with open(absolute_path, 'r') as myfile:
                insert_query = myfile.read()
            clear_with_prefixes = self.add_prefixes_to_query(self.__clear_graph_template, query_file)
            self.handle_request(clear_with_prefixes, endpoint+"/statements", absolute_path)
            query_with_prefixes = self.add_prefixes_to_query(data, query_file)
            response = self.handle_request(query_with_prefixes, endpoint, values_absolute_path)
            results = json.loads(response[1])
            values = []
            try:
                batch_size = int(results['results']['bindings'][0]['batch_size']['value'])
            except:
                batch_size = 100
            logging.info("Batch size: {}".format(batch_size))
            for v in results['results']['bindings']:
                if v['value']['type'] == 'uri':
                    values.append("<{}>".format(v['value']['value']))
                else:
                    values.append('"{}"'.format(v['value']['value']))
            insert_query_with_prefixes = self.add_prefixes_to_query(insert_query, query_file)
            for chunk in self.chunks(values, batch_size):
                query = insert_query_with_prefixes.replace("{{values}}", "\n".join(chunk))
                self.handle_request(query, endpoint+"/statements", absolute_path)
            size = self.get_graph_size(graph=query_file, endpoint=endpoint, query=insert_query_with_prefixes)
            if size > 0:
                self.add_graph_metadata(graph=query_file, endpoint=endpoint+"/statements", triples=size)

    def handle_request(self, query, endpoint, absolute_path):
        logging.info("Executing query: {0}".format(query))
        result = self.execute_query(query, endpoint)
        if not result[0]:
            logging.error("Query execution error for query: {0}\t\tresponse: {1}".format(absolute_path, result[1]))
            raise Exception("Query execution error for query: {0}\t\tresponse: {1}".format(absolute_path, result[1]))
        else:
            return result

    def add_prefixes_to_query(self, query, graph, graph_prefix=True):
        pattern = ""
        if graph_prefix and "http" not in graph:
            pattern = "graph/{0}"
        else:
            pattern = "{0}"
        prefixes = self.query_utils.get_prefixes()
        return "\n"\
            .join([prefixes, query])\
            .replace("{{graph}}", pattern.format(graph))

    def get_clear_graph_template(self):
        return self.__clear_graph_template

    def add_graph_metadata(self, graph, endpoint, triples, graph_prefix=True):
        query = resource_string("common.resources", "graph-metadata.ru")
        query_with_prefix = self.add_prefixes_to_query(query, graph, graph_prefix)
        query_with_versions = query_with_prefix\
            .replace("${{pipeline_version}}", os.environ["VERSION"] if "VERSION" in os.environ else "") \
            .replace("${{dag_version}}", os.environ["DAG_VERSION"] if "DAG_VERSION" in os.environ else "") \
            .replace("${{triples}}", str(triples))
        self.handle_request(query_with_versions, endpoint, "")

    @staticmethod
    def on_status_code(code):
        statuses = {
            200: True,
            204: True
        }
        return statuses.get(code, False)

    def execute_query(self, query, endpoint):
        if 'statements' in endpoint:
            response = requests.post(endpoint, data={'update': query})
        else:
            response = requests.get(endpoint, params={'query': query}, headers={'Accept': 'application/json'})
        return self.on_status_code(response.status_code), response.text


if __name__ == '__main__':
    executor = Executor(QueryUtils())
    # print executor.get_graph_size("http://trr.ontotext.com/resource/graph/tarql/cordisref-FP7programmes.ttl",
    #                                 "http://pascal:8200/repositories/trr-load-test/statements", "")

    executor.execute_folder("/Users/plamentarkalanov/PyCharmProjects/TRR/TRR/sparql-update/matching/authors", "ru", "http://pascal:8200/repositories/trr-load-test/statements")
    # Executor(QueryUtils()).add_graph_metadata("tarql/jrc-names.ttl", "http://pascal:8200/repositories/trr-load-test/statements")
