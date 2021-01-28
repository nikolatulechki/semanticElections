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
infile = "/home/nikola/projects/semanticElections/data/static/sheets/risky_sections.csv"

tarql.execute_query(basePath+"tarql/risky_sections.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_sections.ttl",
                    '-d ,',
                    queryArgs)

