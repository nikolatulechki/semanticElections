# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

queryArgs = {
    "EL": "mi2019" ,
}

basePath = "/home/nikola/projects/semanticElections/data/"

## Coalitions Mapping 2015
infile = "/home/nikola/projects/semanticElections/data/static/sheets/coalitions_mi2015.csv"

tarql.execute_query(basePath+"tarql/coalitions_mi2015.tarql",
                    infile,
                    basePath+"/rdf/mi2015/coalitions_mapping.ttl",
                    '-d ,',
                    queryArgs)


## Coalitions Mapping 2019
infile = "/home/nikola/projects/semanticElections/data/static/sheets/coalitions.csv"

tarql.execute_query(basePath+"tarql/coalitions.tarql",
                    infile,
                    basePath+"/rdf/mi2019/coalitions_mapping.ttl",
                    '-d ,',
                    queryArgs)

## MAIN PARTIES
basePath = "/home/nikola/projects/semanticElections/data/"
infile = "/home/nikola/projects/semanticElections/data/static/sheets/main_parties_wd.csv"

tarql.execute_query(basePath+"tarql/main_party.tarql",
                    infile,
                    basePath+"/rdf/mappings/main_party_mapping.ttl",
                    '-d ,',
                    queryArgs)

