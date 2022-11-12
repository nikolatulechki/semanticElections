# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

queryArgs = {
    "EL": "mi2019" ,
}

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## MAIN PARTIES
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/main_election_data.csv"

tarql.execute_query(basePath+"tarql/main_election_data.tarql",
                    infile,
                    basePath+"rdf/mappings/main_election_data.ttl",
                    '-d ,',
                    queryArgs)

## Coalitions Mapping 2015
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/coalitions_mi2015.csv"

tarql.execute_query(basePath+"tarql/coalitions_mi2015.tarql",
                    infile,
                    basePath+"rdf/mi2015/coalitions_mapping.ttl",
                    '-d ,',
                    queryArgs)


## Coalitions Mapping 2019
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/coalitions_mi2019.csv"

tarql.execute_query(basePath+"tarql/coalitions.tarql",
                    infile,
                    basePath+"rdf/mi2019/coalitions_mapping.ttl",
                    '-d ,',
                    queryArgs)

## MAIN PARTIES
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/main_parties_wd.csv"

tarql.execute_query(basePath+"tarql/main_party.tarql",
                    infile,
                    basePath+"rdf/mappings/main_party_mapping.ttl",
                    '-d ,',
                    queryArgs)

## MAIN PARTY TAGS
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/main_party_tags.csv"

tarql.execute_query(basePath+"tarql/main_party_tags.tarql",
                    infile,
                    basePath+"rdf/mappings/main_party_tags.ttl",
                    '-d ,',
                    queryArgs)

## MUNICIPALITIES
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sheets/mun_wd_mapping.csv"

tarql.execute_query(basePath+"tarql/mun_wd_mapping.tarql",
                    infile,
                    basePath+"rdf/mappings/mun_wd_mapping.ttl",
                    '-d ,',
                    queryArgs)

## SECTIONS_GEOGRAPHY

basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/sections_all.tsv"

tarql.execute_query(basePath+"tarql/sections_geo_wkt.tarql",
                    infile,
                    basePath+"rdf/mappings/section_geography.ttl",
                    '-t',
                    queryArgs)


