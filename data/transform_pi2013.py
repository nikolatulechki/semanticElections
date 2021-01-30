# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS

queryArgs = {
    "YEAR": "2013" ,
    "EL": "pi2013" ,
    "TYP_LABEL": "Парламент на РБ МИР ",
    "EL_LABEL" : "Избори",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2013/pe2013_pe_sections.txt'
tarql.execute_query(basePath+"tarql/sections_pi_13.tarql",
                    infile,
                    basePath+"rdf/pi2013/sections.ttl",
                    '-d ; -H',
                     queryArgs)

## VOTE
queryArgs = {
    "EL": "pi2013" ,
    "TYP" : "" ,
    "RND" : "" ,
    "MV" : "",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2013/pe2013_pe_votes.flat.txt'
tarql.execute_query(basePath+"tarql/votes_pi13.tarql",
                    infile,
                    basePath+"rdf/pi2013/votes.ttl",
                    '-d ; -H',
                    queryArgs)
## PROTOCOLS
queryArgs = {
    "EL": "pi2013" ,
    "TYP" : "" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/pi2013/protokoli/",
    "LINK_PDF" : "https://results.cik.bg/pi2013/pdf/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2013/pe2013_pe_protocols.txt'
tarql.execute_query(basePath+"tarql/protocols_pi2013.tarql",
                    infile,
                    basePath+"rdf/pi2013/protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# # CIK Parties

queryArgs = {
    "EL": "pi2013" ,
    "TYP" : "pi" ,
    "RND" : ""
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2013/pe2013_pe_cikparties.txt'
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/pi2013/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Candidates
queryArgs = {
    "EL": "pi2013" ,
    "TYP" : "pi" ,
    "RND" : "" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/pi2013/pe2013_pe_candidates.txt'
tarql.execute_query(basePath+"tarql/candidate_pi_13.tarql",
                    infile,
                    basePath+"rdf/pi2013/candidates.ttl",
                    '-H -d ;',
                    queryArgs)


