# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2021" ,
    "EL": "pi2021" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори 2021",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/sections_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/sections_pi.tarql",
                    infile,
                    basePath+"rdf/pi2021/sections.ttl",
                    '-d ; -H',
                    queryArgs)
## VOTE
queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/votes_04.04.2021.flat.txt'
tarql.execute_query(basePath+"tarql/votes_pi21.tarql",
                    infile,
                    basePath+"rdf/pi2021/votes.ttl",
                    '-d ; -H',
                    queryArgs)

  ## PREFERENCE
queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/preferences_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/preference_pi21.tarql",
                    infile,
                    basePath+"rdf/pi2021/preferences.ttl",
                    '-d ; -H',
                    queryArgs)

 # PROTOCOLS
queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/pi2021/protokoli/64/",
    "LINK_PDF" : "https://results.cik.bg/pi2021/pdf/64/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/protocols_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2021.tarql",
                    infile,
                    basePath+"rdf/pi2021/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties

queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/cik_parties_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2021/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties

queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "" ,
    "RND" : "",
    "CIK_THR": "31"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/local_parties_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2021/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

# ## Candidates
queryArgs = {
    "EL": "pi2021" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2021/local_candidates_04.04.2021.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2021/candidates.ttl",
                    '-H -d ;',
                    queryArgs)
