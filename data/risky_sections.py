# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())


queryArgs = {
    "EL": "mi2019" ,
}
basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## risky sections
basePath = "/home/nikola/projects/dgood/semanticElections/data/"
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/akf_all_time_risky.csv"

tarql.execute_query(basePath+"tarql/akf_all_time_risky.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_all_time.ttl",
                    '-d ,',
                    queryArgs)

queryArgs = {
    "MODEL": "akf_2022_high_risk" ,
}
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_high_risk.csv"
tarql.execute_query(basePath+"tarql/akf_risky_year.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_akf_2022_high_risk.ttl",
                    '-d ,',
                    queryArgs)

queryArgs = {
    "MODEL": "akf_2022_low_risk",
}
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_low_risk.csv"
tarql.execute_query(basePath+"tarql/akf_risky_year.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_akf_2022_low_risk.ttl",
                    '-d ,',
                    queryArgs)