# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

queryArgs = {
    "EL": "mi2019" ,
}

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

#MI 2019-2022 polygons
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/sofia_geography/section_regions/regions2019_2022.tsv"

tarql.execute_query(basePath+"tarql/sections_sofia_geography.tarql",
                    infile,
                    basePath+"rdf/geo/2019-2022_sofia_wkt.ttl",
                    '-t',
                    queryArgs)

#MI 2023 polygons
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/sofia_geography/section_regions/regions2023.tsv"

tarql.execute_query(basePath+"tarql/sections_sofia_geography.tarql",
                    infile,
                    basePath+"rdf/geo/pi2023_sofia_wkt.ttl",
                    '-t',
                    queryArgs)

# #SOFPLAN GE / NEIGHBORHOODS
#
# basePath = "/home/nikola/projects/dgood/semanticElections/data/"
# infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/sofia_geography/raw/ge_sofplan.csv"
#
# tarql.execute_query(basePath+"tarql/neighborhoods_sofia.tarql",
#                     infile,
#                     basePath+"rdf/geo/neighborhoods_sofia_wkt.ttl",
#                     '-d ,',
#                     queryArgs)
#
#

