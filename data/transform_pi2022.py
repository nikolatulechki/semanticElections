# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2022" ,
    "EL": "pi2022" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори 02 Октомври 2022",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/sections_02.10.2022.txt'
tarql.execute_query(basePath+"tarql/sections_pi22.tarql",
                    infile,
                    basePath+"rdf/pi2022/sections.ttl",
                    '-d ; -H',
                     queryArgs)

# VOTE
queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "true",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/votes_02.10.2022.flat.sum.txt'
tarql.execute_query(basePath+"tarql/votes_mv.tarql",
                    infile,
                    basePath+"rdf/pi2022/votes.ttl",
                    '-d , -H',
                    queryArgs)

# PREFERENCE
queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/preferences_02.10.2022.sum.txt'
tarql.execute_query(basePath+"tarql/preference_mv.tarql",
                    infile,
                    basePath+"rdf/pi2022/preferences.ttl",
                    '-d , -H',
                    queryArgs)

#PROTOCOLS
queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/ns2022/protokoli/64/",
    "LINK_PDF" : "https://results.cik.bg/pvrns2021/tur1/pdf/256/"
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/protocols_02.10.2022.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2022.tarql",
                    infile,
                    basePath+"rdf/pi2022/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties
queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/cik_parties_02.10.2022.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2022/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties

queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "" ,
    "RND" : "",
    "CIK_THR": "36"
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/local_parties_02.10.2022.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2022/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

# Candidates
queryArgs = {
    "EL": "pi2022" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2022/local_candidates_02.10.2022.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2022/candidates.ttl",
                    '-H -d ;',
                    queryArgs)
