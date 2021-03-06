# coding: utf-8

from common.sparql.QueryUtils import QueryUtils
from common.tarql import Tarql


tarql = Tarql(QueryUtils())

basePath = "/home/nikola/projects/semanticElections/data/"

## SECTIONS KO TUR1

queryArgs = {
    "EL": "mi2015" ,
    "EL_LABEL" : "Местни Избори 2015",
    "TYP" : "ko" ,
    "TYP_LABEL" : "кмет на община",
    "RND" : "tur1" ,
    "RND_LABEL" : "Тур 1" ,
    "RND_INT" : "1"

}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/sections_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)
## SECTIONS KO TUR2

queryArgs = {
    "EL": "mi2015" ,
    "EL_LABEL" : "Местни Избори 2015",
    "TYP" : "ko" ,
    "TYP_LABEL" : "кмет на община",
    "RND" : "tur2" ,
    "RND_LABEL" : "Тур 2" ,
    "RND_INT" : "2"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur2/ko/sections_01.11.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/sections_tur.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)

## SECTIONS OS TUR1

queryArgs = {
    "EL": "mi2015" ,
    "EL_LABEL" : "Местни Избори 2015",
    "TYP" : "os" ,
    "TYP_LABEL" : "общински съвет",
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/sections_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"]
tarql.execute_query(basePath+"tarql/sections.tarql",
                    infile,
                    outfilePath+"_sections.ttl",
                    '-d ; -H',
                    queryArgs)

#TODO
# ## SECTIONS GEOGRAPHY
#
# queryArgs = {
#     "EL": "mi2019"
# }
#
# infile = '/home/nikola/projects/semanticElections/data/static/sections/mi2019_sections_geography.csv'
# tarql.execute_query(basePath+"tarql/sections_geo_wkt.tarql",
#                     infile,
#                     basePath+"rdf/mi2019/sections_geography.ttl",
#                     '-d ,',
#                     queryArgs)

## VOTE tur 1
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko/" ,
    "RND" : "tur1/" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/votes_25.10.2015.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE tur 2
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko/" ,
    "RND" : "tur2/" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur2/ko/votes_01.11.2015.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## VOTE os
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "os/" ,
    "RND" : "" ,
    "MV" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/votes_25.10.2015.flat.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/votes.tarql",
                    infile,
                    outfilePath+"_votes.ttl",
                    '-d ; -H',
                    queryArgs)

## PREFERENCE OS
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "os" ,
    "RND" : "" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/preferences_25.10.2015.txt'
tarql.execute_query(basePath+"tarql/preference_os.tarql",
                    infile,
                    basePath+"rdf/mi2015/os_preferences.ttl",
                    '-d ; -H',
                    queryArgs)

## PROTOCOLS KO TUR1
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko/" ,
    "RND" : "tur1/" ,
    "LINK_HTML" : "https://results.cik.bg/minr2015/tur1/protokoli_ko/",
    "LINK_PDF" : "https://results.cik.bg/minr2015/tur1/pdf_ko/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/protocols_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2015.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)


## PROTOCOLS KO TUR2
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko/" ,
    "RND" : "tur2/" ,
    "LINK_HTML" : "https://results.cik.bg/minr2015/tur2/protokoli_ko/",
    "LINK_PDF" : "https://results.cik.bg/minr2015/tur2/pdf_ko/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur2/ko/protocols_01.11.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2015.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)


#TODO
queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "os/" ,
    "RND" : "" ,
    "LINK_HTML" : "https://results.cik.bg/minr2015/tur1/protokoli_os/",
    "LINK_PDF" : "https://results.cik.bg/minr2015/tur1/pdf_os/"
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/protocols_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"].replace("/","") + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/protocols_mi2015.tarql",
                    infile,
                    outfilePath+"_protocols.ttl",
                    '-d ; -H',
                    queryArgs)

# CIK Parties

queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko" ,
    "RND" : "tur1"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/cik_parties_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/cik_parties.tarql",
                    infile,
                    basePath+"rdf/mi2015/cik_parties.ttl",
                    '-H -d ;',
                    queryArgs)

## Local Parties

queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko" ,
    "RND" : "tur1",
    "CIK_THR": "0"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/local_parties_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/mi2015/local_parties.ttl",
                    '-H -d ;',
                    queryArgs)


## Local Parties OS

queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko" ,
    "RND" : "tur1",
    "CIK_THR": "0"
}

infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/local_parties_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/local_parties.tarql",
                    infile,
                    basePath+"rdf/mi2015/local_parties_os.ttl",
                    '-H -d ;',
                    queryArgs)


queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko" ,
    "RND" : "tur1/" ,
}


infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/ko/local_candidates_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)

queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "ko" ,
    "RND" : "tur2/" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur2/ko/local_candidates_01.11.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)

queryArgs = {
    "EL": "mi2015" ,
    "TYP" : "os" ,
    "RND" : "tur1" ,
}
infile = '/home/nikola/projects/semanticElections/gdrive/data/cikOpenData/mi2015/tur1/os/local_candidates_25.10.2015.txt'
outfilePath = basePath + "rdf/" + queryArgs["EL"] + "/" + queryArgs["TYP"] + "_" + queryArgs["RND"].replace("/","")
tarql.execute_query(basePath+"tarql/candidate_os.tarql",
                    infile,
                    outfilePath+"_candidates.ttl",
                    '-H -d ;',
                    queryArgs)


#
# ## Coalitions Mapping
# infile = "/home/nikola/projects/semanticElections/data/static/sheets/coalitions.csv"
#
# tarql.execute_query(basePath+"tarql/coalitions.tarql",
#                     infile,
#                     basePath+"/rdf/mi2019/coalitions_mapping.ttl",
#                     '-d ,',
#                     queryArgs)