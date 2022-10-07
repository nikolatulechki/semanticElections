# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/dgood/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2021" ,
    "EL": "pi2021_11" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори 14 Ноември 2021",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/sections_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/sections_pi.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/sections.ttl",
                    '-d ; -H',
                    queryArgs)
## VOTE
queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "true",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/votes_14.11.2021.flat.txt'
tarql.execute_query(basePath+"tarql/votes_pi21_07.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/votes.ttl",
                    '-d ; -H',
                    queryArgs)

## PREFERENCE
queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/preferences_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/preference_pi21_7.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/preferences.ttl",
                    '-d ; -H',
                    queryArgs)

# PROTOCOLS
queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/pvrns2021/tur1/protokoli/64/",
    "LINK_PDF" : "https://results.cik.bg/pvrns2021/tur1/pdf/256/"
}
infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/protocols_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2021_11.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties

queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/cik_parties_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties

queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "" ,
    "RND" : "",
    "CIK_THR": "36"
}

infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/local_parties_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

# ## Candidates
queryArgs = {
    "EL": "pi2021_11" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/dgood/semanticElections/gdrive/data/cikOpenData/pi2021_11/local_candidates_14.11.2021.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2021_11/candidates.ttl",
                    '-H -d ;',
                    queryArgs)
