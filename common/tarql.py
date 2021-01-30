import subprocess
import tempfile
import logging
import argparse
from common.sparql.QueryUtils import QueryUtils
from common import graphdb
import os
from common.configuration.Configuration import Configuration


class Tarql:

    def __init__(self, query_utils):
        self.query_utils = query_utils

    def execute_query(self, query_path, file_path, output_path, args, queryargs):
        logging.info("Processing File" + file_path)

        temp = tempfile.NamedTemporaryFile(mode='w')
        with open(query_path, "r") as f:
            query = f.read()
        for k, v in queryargs.items():
            rep = "{{{}}}".format(k)
            query = query.replace(rep, v)
        command = ["/home/nikola/source/tarql-1.2/bin/tarql"] + args.split(" ") + [temp.name, file_path]
        temp.write("\n".join([self.query_utils.get_prefixes(), query]))
        temp.flush()
        with open(output_path, "w") as out:
            proc = subprocess.Popen(command, stdout=out, stderr=subprocess.PIPE)
            output, err = proc.communicate()

            if len(err) > 0:
                logging.error("TARQL execution error for file {} \nError: {}".format(query_path, err))
                raise Exception("TARQL execution error for file {} \nError: {}".format(query_path, err))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tarql wrapper')
    parser.add_argument('args', type=str, help='tarql arguments')
    parser.add_argument('query', type=str, help='path to the tarql query')
    parser.add_argument('csv', type=str, help='path to the csv file')
    parser.add_argument('output', type=str, help='path to the output ttl file')

    args = parser.parse_args()

    tarql = Tarql(QueryUtils())
    tarql.execute_query(args.query, args.csv, args.output, args.args)

    # gdb_import = Configuration().get_config().get("os", "graphdb_import_dir")
    # filename = args.output.replace(gdb_import, "")
    # graphdb.replace_graph(filename, "{}graph/{}".format(tarql.query_utils.get_base_uri(), filename))
