# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

queryArgs = {
    "EL": "mi2019" ,
}

basePath = "/home/nikola/projects/semanticElections/data/"

## risky sections
basePath = "/home/nikola/projects/semanticElections/data/"
infile = "/home/nikola/projects/semanticElections/analysis/akf/risky_2021/11-2021/risky-low.csv"

tarql.execute_query(basePath+"tarql/risky_sections.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_2021-11_low.ttl",
                    '-d ,',
                    queryArgs)

