# SOFIA PROFILING

Compute arbitrary rule based counts at the polling station level
Each query observations to the `<cube/sofia-profiling>` cube in a separate graph

## PPDB-core

Voted for PPDB in  pi2023

## GERB-core

MIN voted GERB

## UNVOTEd-core

min(voters-voted)

## CSV download

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@results_drilldown.rq' 'https://elections.ontotext.com/repositories/elections' > data/sofia_cores.csv
```

# YasGui visual expo;oration

[LINK]()

```sparql
BASE  <https://elections.ontotext.com/resource/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX myc: <https://elections.ontotext.com/resource/prop/cube/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX section: <https://elections.ontotext.com/resource/section/>

SELECT *
WHERE {


    {select distinct ?sec ?GE ?region ?address ?SECTION 
        where {
            ?sec a my:Section ; ^myc:locality/qb:dataSet <cube/sofia-profiling> .
            optional{
                ?sec myd:matched_section/^myd:matched_section ?mi19sec ; myd:streetAddress ?address.
                ?mi19sec myd:main_election election:mi2019 ; myp:neighborhood [mypq:isPrimary true ; myps:neighborhood/rdfs:label ?GE] ; myd:number ?num ; geo:hasGeometry/geo:asWKT ?SECTION .
                bind(substr(?num,5,2) as ?region)
            }
        }
	}

    ?v myd:section ?sec ; myd:main_election election:pi2023 ; myd:voters_count ?voters23_count ; myd:voters_voted_count ?voted23_count .
    [myc:locality ?sec ; myc:candidate "gerb-core" ; myc:votes ?gerb_core] .
    [myc:locality ?sec ; myc:candidate "dps-core" ;  myc:votes ?dps_core] .
    [myc:locality ?sec ; myc:candidate "ppdb" ; myc:votes ?ppdb_core] .
    [myc:locality ?sec ; myc:candidate "patriot-core" ; myc:votes ?patriot_core] .
    [myc:locality ?sec ; myc:candidate "socleft-core" ; myc:votes ?socleft_core] .
    [myc:locality ?sec ; myc:candidate "unvoted-core" ; myc:votes ?unvoted_core] .
    [myc:locality ?sec ; myc:candidate "swing" ; myc:votes ?swing] .
    ?v myd:section ?sec ; myd:link_html ?protocol .
   
  	
  
    bind(concat(
     "number: ",strafter(str(?sec),str(section:)),"\n",
     "swing: ",str(?swing),"\n",
     "gerb-core: ",str(?gerb_core),"\n",
     "dps-core: ",str(?dps_core),"\n",
     "ppdb: ",str(?ppdb_core),"\n",      
     "patriot-core: ",str(?patriot_core),"\n",
     "socleft-core: ",str(?socleft_core),"\n",
     "unvoted-core: ",str(?unvoted_core),"\n",
     "voters_23: ",str(?voters23_count),"\n",
     "voted_23: ",str(?voted23_count),"\n"
    ) as ?SECTIONLabel)  
  
   bind(concat("jet,",str(?ppdb_core/?voted23_count*1.5)) as ?SECTIONColor) #controls coloring of polygons, use the multiplier to control intensity fro smaller ratios
 
}
```