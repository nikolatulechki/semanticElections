# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS KO TUR1

queryArgs = {
    "EL": "mi2019" ,
    "EL_LABEL" : "Местни Избори 2019",
    "TYP" : "ko" ,
    "TYP_LABEL" : "кмет на община",
    "RND" : "tur1" ,
    "RND_LABEL" : "Тур 1" ,
    "RND_INT" : "1"

}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/sections_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)
## SECTIONS KO TUR2

queryArgs = {
    "EL": "mi2019" ,
    "EL_LABEL" : "Местни Избори 2019",
    "TYP" : "ko" ,
    "TYP_LABEL" : "кмет на община",
    "RND" : "tur2" ,
    "RND_LABEL" : "Тур 2" ,
    "RND_INT" : "2"

}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur2/ko/sections_03.11.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)

## SECTIONS OS TUR1

queryArgs = {
    "EL": "mi2019" ,
    "EL_LABEL" : "Местни Избори 2019",
    "TYP" : "os" ,
    "TYP_LABEL" : "общински съвет",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/sections_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"]
tarql.execute_query(basePath+"tarql/sections.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)

## SECTIONS GEOGRAPHY

queryArgs = {
    "EL": "mi2019"
}

infile = '/home/nikola/projects/semanticElections/data/static/sections/mi2019_sections_geography.csv'
tarql.execute_query(basePath+"tarql/sections_geo_wkt.tarql",
                    infile,
                    basePath+"rdf/mi2019/sections_geography.ttl",
                    '-d ,',
                    queryArgs)

## VOTE tur 1
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko/" ,
    "RND" : "tur1/" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/votes_27.10.2019.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE tur 2
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko/" ,
    "RND" : "tur2/" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur2/ko/votes_03.11.2019.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE os
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "os/" ,
    "RND" : "" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/votes_27.10.2019.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## PROTOCOLS KO TUR1
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko/" ,
    "RND" : "tur1/" ,
    "LINK_HTML" : "https://results.cik.bg/mi2019/tur1/protokoli/2/",
    "LINK_PDF" : "https://results.cik.bg/mi2019/tur1/pdf/2/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/protocols_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2019.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)

## PROTOCOLS KO TUR2
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko/" ,
    "RND" : "tur2/" ,
    "LINK_HTML" : "https://results.cik.bg/mi2019/tur2/protokoli/2/",
    "LINK_PDF" : "https://results.cik.bg/mi2019/tur2/pdf/2/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur2/ko/protocols_03.11.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2019.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)

## PROTOCOLS OS
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "os/" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/mi2019/tur1/protokoli/1/",
    "LINK_PDF" : "https://results.cik.bg/mi2019/tur1/pdf/1/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/protocols_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2019.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)


 ## PREFERENCE OS
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "os" ,
    "RND" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/preferences_27.10.2019.txt'
tarql.execute_query(basePath+"tarql/preference_os.tarql",
                    infile,
                    basePath+"rdf/mi2019/os_preferences.ttl",
                    '-d ; -H',
                    queryArgs)



# CIK Parties

queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko" ,
    "RND" : "tur1"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/cik_parties_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/mi2019/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Local Parties

queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko" ,
    "RND" : "tur1",
    "CIK_THR": "66"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/local_parties_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/mi2019/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Local Parties

queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "os" ,
    "RND" : "tur1",
    "CIK_THR": "66"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/local_parties_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/mi2019/local_parties_os.ttl",
                    '-H -d ;',
                    queryArgs)
##CANDIDATES

queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko" ,
    "RND" : "tur1/" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/ko/local_candidates_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)
##CANDIDATES

queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "ko" ,
    "RND" : "tur2/" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur2/ko/local_candidates_03.11.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)


##CANDIDATES OS
queryArgs = {
    "EL": "mi2019" ,
    "TYP" : "os" ,
    "RND" : "tur1" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2019/tur1/os/local_candidates_27.10.2019.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate_os.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)

## Coalitions Mapping
infile = "/home/nikola/projects/semanticElections/data/static/sheets/coalitions.csv"

tarql.execute_query(basePath+"tarql/coalitions.tarql",
                    infile,
                    basePath+"/rdf/mi2019/coalitions_mapping.ttl",
                    '-d ,',
                    queryArgs)