import requests
from common.configuration.Configuration import Configuration
import re
import json
import time
import logging
from common.sparql.QueryUtils import QueryUtils
from common.sparql.Executor import Executor


def replace_graph(filename, graph, endpoint=Configuration().get_config().get("sparql", "endpoint_elections")):
    query = {
        "fileNames": [
            filename
        ],
        "importSettings": {
            "context": graph,
            "replaceGraphs": [
                graph
            ]
        }
    }

    headers = {'Content-Type': 'application/json'}

    parts = re.findall("^(.*)/repositories/(.*)", endpoint)

    import_endpoint = "{}/rest/data/import/server/{}" \
        .format(parts[0][0], parts[0][1])
    logging.info("Sending file for import: {} \nEndpoint: {}".format(filename, import_endpoint))
    response = requests.post(import_endpoint, data=json.dumps(query), headers=headers)

    if response.status_code != 202:
        raise Exception("Unable to send ttl for import: {} \n Response: ".format(filename, response.text))

    while True:
        status = json.loads(requests.get(import_endpoint).text)
        for x in status:
            if x["name"] == filename:
                if x["status"] in ["IMPORTING", "PENDING"]:
                    time.sleep(5)
                elif x["status"] == "DONE":
                    executor = Executor(QueryUtils())
                    size = executor.get_graph_size(graph=graph, endpoint=endpoint, query="")
                    executor.add_graph_metadata(graph, "/".join([endpoint, "statements"]),
                                                graph_prefix=False,
                                                triples=size)
                    return
                else:
                    raise Exception("Import error for ttl file: {}".format(filename))


if __name__ == '__main__':
    pass
    #replace_graph("tarql/project.ttl", "http://trr.ontotext.com/resource/graph//opt/graphdb-import/tarql/project.ttl")
