# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS

queryArgs = {
    "EL": "ep2019" ,
    "TYP" : "ep",
    "TYP_LABEL": "Европейски Парламент 2019",
    "EL_LABEL" : "Избори за Европейски Парламент 2019",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/ep2019/sections.txt'
tarql.execute_query(basePath+"tarql/sections_ep.tarql",
                    infile,
                    basePath+"rdf/ep2019/sections.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE
queryArgs = {
    "EL": "ep2019" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/ep2019/votes.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/ep2019/votes.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE_MV
queryArgs = {
    "EL": "ep2019" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "/mv",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/ep2019/votes_mv.flat.txt'
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    basePath+"rdf/ep2019/votes_mv.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties

queryArgs = {
    "EL": "ep2019" ,
    "TYP" : "ep" ,
    "RND" : ""
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/ep2019/cik_parties.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/ep2019/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)

queryArgs = {
    "EL": "ep2019" ,
    "TYP" : "ep" ,
    "RND" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/ep2019/cik_candidates.txt'
tarql.execute_query(basePath+"tarql/candidate_ep.tarql",
                    infile,
                    basePath+"rdf/ep2019/candidates.ttl",
                    '-H -d ;',
                    queryArgs)

# TODO PROTOCOLS

