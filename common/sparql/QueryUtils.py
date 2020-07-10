import rdflib
import logging
from rdflib.exceptions import Error
import re
from pkg_resources import resource_filename


class QueryUtils:
    __prefixes = rdflib.Graph()
    __base_uri = ""

    def __init__(self):
        self.set_prefixes(resource_filename("model", "prefixes.ttl"))

    def set_prefixes(self, path):
        try:
            self.__prefixes = rdflib.Graph()
            self.__prefixes.parse(path, format="ttl")
            self.__base_uri = self.__extract_base__(path)
        except Error:
            logging.error("Prefix file {} not found".format(path))

    def get_prefixes(self):
        return str.join("\n",
                        [self.__base_uri] + ["PREFIX {}: <{}>".format(x, y) for x, y in self.__prefixes.namespaces()])

    def get_base_uri(self):
        return re.findall("<(.*)>", self.__base_uri)[0]

    def __extract_base__(self, path):
        with open(path, 'r') as f:
            for line in f.readlines():
                if "@base" in line:
                    return self.__ttl_prefix_to_rq__(line)

    @staticmethod
    def __ttl_prefix_to_rq__(line):
        return re.sub("^@|\.(\s+)?$", "", line)

