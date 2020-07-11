# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS KO TUR1

queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr",
    "TYP_LABEL": "Президент и Вицепрезидент",
    "EL_LABEL" : "Избори",
    "RND": "tur1",
    "RND_LABEL": "Тур 1",
    "RND_INT": "1"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur1/sections_06.11.2016.txt'
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/sections_tur1.ttl",
                    '-d ; -H',
                    queryArgs)
## VOTE
queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr",
    "TYP_LABEL": "Президент и Вицепрезидент",
    "EL_LABEL" : "Избори",
    "RND": "tur2",
    "RND_LABEL": "Тур 2",
    "RND_INT": "2"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur2/sections_13.11.2016.txt'
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/sections_tur2.ttl",
                    '-d ; -H',
                    queryArgs)

raise Exception()
# CIK Parties

queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2017/cik_parties_26.03.2017.txt'
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

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2017/local_parties_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/pi2017/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Candidates
queryArgs = {
    "EL": "pi2017" ,
    "TYP" : "" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2017/local_candidates_26.03.2017.txt'
tarql.execute_query(basePath+"tarql/candidate_pi.tarql",
                    infile,
                    basePath+"rdf/pi2017/candidates.ttl",
                    '-H -d ;',
                    queryArgs)

# TODO PROTOCOLS

