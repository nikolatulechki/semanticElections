# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS KO TUR2

queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr",
    "EL_LABEL" : "Избори за Президент и Вицепрезидент",
    "RND": "tur1/",
    "RND_LABEL": "Тур 1",
    "RND_INT": "1"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur1/sections_06.11.2016.txt'
tarql.execute_query(basePath+"tarql/sections_pvnr.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/sections_tur1.ttl",
                    '-d ; -H',
                    queryArgs)

## SECTIONS TUR2

queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr",
    "EL_LABEL" : "Избори за Президент и Вицепрезидент",
    "RND": "tur1/",
    "RND_LABEL": "Тур 2",
    "RND_INT": "2"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur2/sections_13.11.2016.txt'
tarql.execute_query(basePath+"tarql/sections_pvnr.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/sections_tur2.ttl",
                    '-d ; -H',
                    queryArgs)


# CIK Parties

queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr" ,
    "RND" : ""
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur1/cik_candidates_06.11.2016.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)

# Candidates TUR1

queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr" ,
    "RND" : "tur1"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur1/cik_candidates_06.11.2016.txt'
tarql.execute_query(basePath+"tarql/candidate_pvnr.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/candidates_tur1.ttl",
                    '-H -d ;',
                    queryArgs)

# Candidates TUR2
queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "pvnr" ,
    "RND" : "tur1/"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur2/cik_candidates_13.11.2016.txt'
tarql.execute_query(basePath+"tarql/candidate_pvnr.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/candidates_tur2.ttl",
                    '-H -d ;',
                    queryArgs)

## VOTE TUR1
queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "",
    "RND": "tur1/",
    "RND_LABEL": "Тур 1",
    "RND_INT": "1",
    "MV" : ""
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur1/votes_06.11.2016.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/votes_tur1.ttl",
                    '-d ; -H',
                    queryArgs)


## VOTE TUR2
queryArgs = {
    "EL": "pvnr2016" ,
    "TYP" : "",
    "RND": "tur2/",
    "RND_LABEL": "Тур 2",
    "RND_INT": "2",
    "MV" : ""
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pvnr2016/tur2/votes_13.11.2016.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/pvnr2016/votes_tur2.ttl",
                    '-d ; -H',
                    queryArgs)

# TODO PROTOCOLS


