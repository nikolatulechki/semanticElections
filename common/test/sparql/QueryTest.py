from rdflib import Graph, ConjunctiveGraph


class QueryTest:
    __input_graph = ConjunctiveGraph()
    __expected_graph = Graph()
    __test_graph_name = "http://test.com"

    def __init__(self, input_file, output_file, file_format, query):
        self.__input_graph.parse(input_file, format=file_format)
        self.__expected_graph.parse(output_file, format=file_format)
        self.__query = query.replace("{{graph}}", self.__test_graph_name)

    def get_input_graph(self):
        return self.__input_graph

    def get_expected_graph(self):
        return self.__expected_graph

    def get_query(self):
        return self.__query

    def execute_update_query(self):
        self.__input_graph.update(self.__query)
        get_result_query = "construct { ?s ?p ?o } where { graph <{{g}}>  { ?s ?p ?o }}"\
            .replace("{{g}}", self.__test_graph_name)
        new_graph = self.__input_graph.query(get_result_query)
        return sorted(list(self.__expected_graph)), sorted(list(new_graph))