# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2017" ,
    "EL": "pi2017" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/sections_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/sections_pi.tarql",
                    infile,
                    basePath+"rdf/pi2017/sections.ttl",
                    '-d ; -H',
                    queryArgs)
## VOTE
queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/votes_26.03.2017.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/pi2017/votes.ttl",
                    '-d ; -H',
                    queryArgs)

 ## PREFERENCE
queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/preferences_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/preference.tarql",
                    infile,
                    basePath+"rdf/pi2017/preferences.ttl",
                    '-d ; -H',
                    queryArgs)

## PROTOCOLS
queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/pi2017/protokoli/",
    "LINK_PDF" : "https://results.cik.bg/pi2017/pdf/"
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/protocols_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2017.tarql",
                    infile,
                    basePath+"rdf/pi2017/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties

queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/cik_parties_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2017/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties

queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "" ,
    "RND" : "",
    "CIK_THR": "21"
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/local_parties_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2017/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Candidates
queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2017/local_candidates_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2017/candidates.ttl",
                    '-H -d ;',
                    queryArgs)

# TODO PROTOCOLS

