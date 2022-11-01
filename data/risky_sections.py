# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())


queryArgs = {
    "EL": "mi2019" ,
}
basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## risky sections
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/akf_all_time_risky.csv"
queryArgs = {
    "MODEL": "all_time_risky" ,
}
tarql.execute_query(basePath+"tarql/risky_matched_section.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_all_time.ttl",
                    '-d ,',
                    queryArgs)


infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_high_risk_absvalue.csv"
queryArgs = {
    "MODEL": "2022_high_abs_values" ,
}
tarql.execute_query(basePath+"tarql/risky_matched_section.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_2022_high_abs_values.ttl",
                    '-d ,',
                    queryArgs)


infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_low_risk_absvalue.csv"
queryArgs = {
    "MODEL": "2022_low_abs_values" ,
}
tarql.execute_query(basePath+"tarql/risky_matched_section.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_2022_low_abs_values.ttl",
                    '-d ,',
                    queryArgs)




queryArgs = {
    "MODEL": "akf_2022_high_risk" ,
}
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_high_risk.csv"
tarql.execute_query(basePath+"tarql/risky_single_section.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_2022_high_risk.ttl",
                    '-d ,',
                    queryArgs)

queryArgs = {
    "MODEL": "akf_2022_low_risk",
}
infile = "/home/nikola/projects/dgood/semanticElections/data/static/sections/risky/2022_low_risk.csv"
tarql.execute_query(basePath+"tarql/risky_single_section.tarql",
                    infile,
                    basePath+"rdf/mappings/risky_akf_2022_low_risk.ttl",
                    '-d ,',
                    queryArgs)