# coding: utf-8
import os
from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

path = basePath+"static/sections/akf_mappings"
for infile in os.listdir(path):
    if infile.endswith(".csv"):
        el_str = infile.replace(".csv","")
        queryArgs = {
            "EL" : el_str
        }
        tarql.execute_query(basePath+"tarql/matched_sections_akf.tarql",
                            f"{path}/{infile}",
                            basePath+"rdf/mappings/akf_sections/"+el_str+".ttl",
                            '-d ,',
                            queryArgs)


