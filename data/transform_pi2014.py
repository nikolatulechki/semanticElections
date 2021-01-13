# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

# ## SECTIONS
#
# queryArgs = {
#     "YEAR": "2014" ,
#     "EL": "pi2014" ,
#     "TYP_LABEL": "Парламент на РБ МИР ",
#     "EL_LABEL" : "Избори",
# }
# infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/sections_pe2014.txt'
# tarql.execute_query(basePath+"tarql/sections_pi_14.tarql",
#                     infile,
#                     basePath+"rdf/pi2014/sections.ttl",
#                     '-d ; -H',
#                     queryArgs)

## VOTE
queryArgs = {
    "EL": "pi2014" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/votes_pe2014.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/pi2014/votes.ttl",
                    '-d ; -H',
                    queryArgs)

#  ## PREFERENCE
# queryArgs = {
#     "EL": "pi2014" ,
#     "TYP" : "" ,
#     "RND" : "" ,
#     "MV" : "",
# }
# infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/preferences_pe2014.txt'
# tarql.execute_query(basePath+"tarql/preference.tarql",
#                     infile,
#                     basePath+"rdf/pi2014/preferences.ttl",
#                     '-d ; -H',
#                     queryArgs)
# #

## PROTOCOLS
queryArgs = {
    "EL": "pi2014" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/pi2014/protokoli/",
    "LINK_PDF" : "https://results.cik.bg/pi2014/pdf/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/protocols_pe2014.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2014.tarql",
                    infile,
                    basePath+"rdf/pi2014/protocols.ttl",
                    '-d ; -H',
                    queryArgs)
#
# # CIK Parties
#
# queryArgs = {
#     "EL": "pi2014" ,
#     "TYP" : "pi" ,
#     "RND" : ""
# }
#
# infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/parties_pe2014.txt'
# tarql.execute_query(basePath+"tarql/cik_parties.tarql",
#                     infile,
#                     basePath+"rdf/pi2014/cik_parties.ttl",
#                     '-H -d ;',
#                     queryArgs)


# ## Local Parties
#
# queryArgs = {
#     "EL": "pi2017" ,
#     "TYP" : "" ,
#     "RND" : "",
#     "CIK_THR": "21"
# }
#
# infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/ind_pe2014.txt'
# tarql.execute_query(basePath+"tarql/local_parties.tarql",
#                     infile,
#                     basePath+"rdf/pi2014/ind.ttl",
#                     '-H -d ;',
#                     queryArgs)
#

## Candidates
queryArgs = {
    "EL": "pi2014" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2014/candidates_pe2014.txt'
tarql.execute_query(basePath+"tarql/candidate_pi_14.tarql",
                    infile,
                    basePath+"rdf/pi2014/candidates.ttl",
                    '-H -d ;',
                    queryArgs)


