# coding: utf-8
import sys
from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2023" ,
    "EL": "pi2023" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори 02 Април 2023",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/sections_02.04.2023.txt'
tarql.execute_query(basePath+"tarql/sections_pi22.tarql",
                    infile,
                    basePath+"rdf/pi2023/sections.ttl",
                    '-d ; -H',
                     queryArgs)

# VOTE
queryArgs = {
    "EL": "pi2023" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "true",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/votes_02.04.2023.flat.txt'
tarql.execute_query(basePath+"tarql/votes_mixed.tarql",
                    infile,
                    basePath+"rdf/pi2023/votes.ttl",
                    '-d ; -H',
                    queryArgs)


# # PREFERENCE
# queryArgs = {
#     "EL": "pi2023" ,
#     "TYP" : "" ,
#     "RND" : "" ,
#     "MV" : "",
# }
# infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/preferences_02.04.2023.txt'
# tarql.execute_query(basePath+"tarql/preference_mixed.tarql",
#                     infile,
#                     basePath+"rdf/pi2023/preferences.ttl",
#                     '-d ; -H',
#                     queryArgs)

#PROTOCOLS
queryArgs = {
    "EL": "pi2023" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/ns2023/protokoli/64/",
    "LINK_PDF" : "https://results.cik.bg/ns2023/pdf/64/"
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/protocols_02.04.2023.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2023.tarql",
                    infile,
                    basePath+"rdf/pi2023/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties
queryArgs = {
    "EL": "pi2023" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/cik_parties_02.04.2023.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2023/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties

queryArgs = {
    "EL": "pi2023" ,
    "TYP" : "" ,
    "RND" : "",
    "CIK_THR": "36"
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/local_parties_02.04.2023.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2023/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

# Candidates
queryArgs = {
    "EL": "pi2023" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2023/local_candidates_02.04.2023.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2023/candidates.ttl",
                    '-H -d ;',
                    queryArgs)
