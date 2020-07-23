# Preference votes

## Sum pref of midlist candidates

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?cand ?c_lab ?p_lab (sum(?votes) as ?votes_sum) where { 
	?s a my:PreferenceVote ; mypq:valid_votes_recieved ?votes ; myps:preference_vote ?cand .
    ?cand myd:number ?cand_num ; rdfs:label ?c_lab .
    ?cand myd:represents ?party .
    ?party myd:number ?party_num ; rdfs:label ?p_lab .
    filter(?cand_num>10)
    filter(?votes>10)
    filter(?cand_num != ?party_num)
} group by ?cand ?c_lab ?p_lab order by desc(?votes_sum) 
```



## Place level aggregations for 2 parties 

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>

# wd:Q133968 GERB
# wd:Q164242 DPS


PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select * {
    
bind((?GERB19/?ALLVOTE19 - ?GERB15/?ALLVOTE15) as ?GRTHGERB19)
bind((?DPS19/?ALLVOTE19 - ?DPS15/?ALLVOTE15) as ?GRTHDPS19)
    
{select ?place ?label (sum(?anyvote15) as ?ALLVOTE15) (sum(?gerbvotes15) as ?GERB15) (sum(?dpsvotes15) as ?DPS15) (sum(?anyvote19) as ?ALLVOTE19) (sum(?gerbvotes19) as ?GERB19) (sum(?dpsvotes19) as ?DPS19) 

where { 
    {
        select ?place {
            ?place a my:Place ;
        } limit 100
    } 
    ?place a my:Place ; rdfs:label ?label .
    {
    ?sec15 a my:Section ; myd:place ?place .
 
    ?voting15 myd:section ?sec15 ; myd:election/myd:partOf <election/mi2015/os> .
    ?voting15 myp:vote ?vote15 .
    ?vote15 mypq:valid_votes_recieved ?anyvote15 ; myps:vote ?party15 .

    bind(if(exists{?party15 myd:party+ wd:Q133968},?anyvote15,0) as  ?gerbvotes15)
    bind(if(exists{?party15 myd:party+ wd:Q164242},?anyvote15,0) as  ?dpsvotes15)
    }
    UNION
    {
    ?sec19 a my:Section ; myd:place ?place .
    ?voting19 myd:section ?sec19 ; myd:election/myd:partOf <election/mi2019/os> .
    ?voting19 myp:vote ?vote19 .
    ?vote19 mypq:valid_votes_recieved ?anyvote19 ; myps:vote ?party19 .

    bind(if(exists{?party19 myd:hasPart?/myd:party+ wd:Q133968},?anyvote19,0) as  ?gerbvotes19)
    bind(if(exists{?party19 myd:hasPart?/myd:party+ wd:Q164242},?anyvote19,0) as  ?dpsvotes19)
    }
}
group by ?place ?label}
}

```

## Buisness Questions

### Секции с над 80% избирателна активност.

```sparql
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
    ?vot a my:Voting ; 
         myd:voters_count ?voters_reg ;
         myd:voters_additional_count ?voters_add ;
         myd:votes_valid_count ?valid_votes ; 
         myd:votes_invalid_count ?invalid_votes ;
         myd:linkProtocol ?prot ;
         myd:linkScanned ?pdf ;
         myd:section/rdfs:label ?section_label ;
    	 rdfs:label ?vote_label ;
    	
	. 
    bind(?voters_reg+?voters_add as ?voters_tot)
    bind(?valid_votes/?voters_tot as ?voting_activity)
    bind(?invalid_votes/?voters_tot as ?invalid_ratio)
}  
order by desc(?invalid_ratio) 
limit 1000
```

### Обърнато Гласуване

- 150-те секции, в които има "обърнато" гласуване между 1 и 2 тур за кмет.
- какво значи по-точно?
- примерно - на първи тур е бил Х с повече гласове, но на втори Y събира повече от него

```sparql
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
select distinct ?election_label ?section_label ?cand1_name ?cand2_name ?cand1_label ?cand2_label ?votes_tur1_c1 ?votes_tur1_c2 ?votes_tur2_c1 ?votes_tur2_c2 ?winner ?t1_ratio ?t2_ratio {
    ?voting2 a my:Voting ;
             myd:round 2 ;
             myd:section ?section ;
             myd:partOf/myd:partOf ?election ;
                       myd:vote ?cand1, ?cand2 .
    filter(str(?cand1)>str(?cand2))
    
    ?election rdfs:label ?election_label .
    ?section rdfs:label ?section_label .
    ?voting2 myp:vote ?v2c1 , ?v2c2 .
    ?v2c1 mypq:valid_votes_recieved ?votes_tur2_c1 ;
          myps:vote ?cand1 .
    ?v2c2 mypq:valid_votes_recieved ?votes_tur2_c2 ;
          myps:vote ?cand2 .
    
    ?voting1 a my:Voting ;
             myd:round 1 ;
             myd:section ?section ;
             myd:partOf/myd:partOf  ?election ;
                       myd:vote ?cand1, ?cand2 ;
    .
    ?voting1 myp:vote ?v1c1 , ?v1c2 .
    ?v1c1 mypq:valid_votes_recieved ?votes_tur1_c1 ;
          myps:vote ?cand1 ;
    .
    ?v1c2 mypq:valid_votes_recieved ?votes_tur1_c2 ;
          myps:vote ?cand2 ;
     .
    ## candidate party labels 
    ?cand1 rdfs:label ?cand1_label .
    ?cand2 rdfs:label ?cand2_label .
    
    ## candidate name 
    
    
    
    bind(if(?votes_tur2_c1>?votes_tur2_c2,?cand1_name,?cand2_name) as ?winner)
    
    bind(?votes_tur1_c1/?votes_tur1_c2 as ?t1_ratio)
    bind(?votes_tur2_c1/?votes_tur2_c2 as ?t2_ratio)
    filter ((?t1_ratio < 1 && ?t2_ratio > 1) || (?t1_ratio > 1 && ?t2_ratio < 1) )
    
    ?cand1 ^mypq:represents ?csy1 .
    ?csy1 myps:candidacy/myd:partOf ?election ; ^myp:candidacy/rdfs:label ?cand1_name .      
    
    ?cand2 ^mypq:represents ?csy2 .
    ?csy2 myps:candidacy/myd:partOf ?election ; ^myp:candidacy/rdfs:label ?cand2_name .       
    
}
```

### Top 1000K votes for a given party

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>        
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mys: <https://github.com/nikolatulechki/semanticElections/resource/entity/statement/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?section_label ?voting_label ?vote_party ?vote_total ?vote_ratio ?protocol
where { 
    bind(<party/56> as ?party)
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:votes_valid_count ?vote_total ;
        myp:vote ?vote ;
        myd:section/rdfs:label ?section_label ;
        myd:linkProtocol ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          myps:vote/myd:hasPart? ?party ;
          myps:vote/rdfs:label ?party_label ;                       
    .
    bind(?vote_party/?vote_total as ?vote_ratio)
} order by desc(?vote_ratio) limit 1000
```

# Postprocessing queries 

## Query to clean-up broken labels 
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
delete {?s rdfs:label ?label}
#select *
where { 
    ?s rdfs:label ?label .
    filter(contains(?label,"��"))
    {select ?s (count(*) as ?c) where {
        ?s rdfs:label ?label . 
        } group by ?s having(?c>1) }
} 
```

## fix double party types +

```sparql
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
delete {
    ?party myd:type "independant" } 
where { 
    ?party a my:Party ; myd:type "local_coalition" .
}
```

### GEN MI2015 localparty mappings

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?loc (group_concat(distinct ?num;separator=";") as ?nums) where { 
	?loc a my:LocalParty ; rdfs:label ?locLabel  ; myd:candidacy/myd:partOf+ election:mi2015 .
    ?main a my:ElectionParty ; rdfs:label ?mainLabel ; myd:candidacy election:mi2015 ; myd:number ?num .
    filter(contains(lcase(?locLabel),lcase(?mainLabel)))
    filter(!sameterm(?main,<party/mi2015/75>)) #шибаните зелени
} group by ?loc
```

### Candidate Matching query 

### Names not following the main pattern 
```
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>        
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * 
where { 
    ?c1 a my:Candidate ; rdfs:label ?l1 .
    filter(!regex(?l1, "^[^ ]+ [^ ]+ [^ ]+$","i"))
} 
```

## Geography 

nearby voting places

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
select * where { 
    bind(<votingPlace/e4a01f0684b5a1bfbf45a2ae5b846ece5bf9e5f7> as ?p1)
#	?p1 a my:Place .
    ?p2 a my:VotingPlace .  
    ?p1 geo:location/geo:lat ?lat1 ; geo:location/geo:long ?long1 .
    ?p2 geo:location ?geo2 .
    ?geo2 omgeo:nearby(?lat1 ?long1 "10km")
} limit 100 
```

federation for wikidata places and their GEO

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
prefix wdt: <http://www.wikidata.org/prop/direct/> 

insert {
    graph my:wg-geo-graph {
   	 	?p myd:wdMatch ?q ; geo:location ?POINT .
    	?POINT a geo:Point ; geo:asWKT ?geo .
    }
}
where { 
 	?p a my:Place ; myd:ekatte ?ekatte .
    service <https://query.wikidata.org/sparql> {
        ?q wdt:P3990 ?ekatte ; wdt:P625 ?geo 
    }
    bind(uri(concat(str(?p),"/geo")) as ?POINT)
}
```

Comparing distance of voting places with center pof place in order to repair google geomatching

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX uom: <http://www.opengis.net/def/uom/OGC/1.0/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
#    bind(<place/02676> as ?p1)
    {
        select ?p1 {
            ?vp a my:VotingPlace ; myd:place ?p1. 
        } group by ?p1 having (count(?vp) = 0)
    }
    ?p1 a my:Place ; rdfs:label ?placeLabel .
    ?vp a my:VotingPlace ; myd:place ?p1 ; rdfs:label ?vpLabel .
    ?vp geo:hasGeometry/geo:asWKT ?vpgeo .
    ?p1 geo:hasGeometry/geo:asWKT ?pgeo .
    bind(strdt(str(?vpgeo),<http://www.opengis.net/ont/geosparql#wktLiteral>) as ?newgeo)
    bind(geof:distance(?pgeo, ?newgeo, uom:metre) as ?dist)
    filter(?dist > 15000)
} #limit 100 
```

Postprocessing Q to fix voting places positioned far from their parent places. Fallback solution is to place them at the same location as their parent place. Will add a flag so that eventually we can look and fix them directly in Wikidata.

# Aggregation Queries

Local elections - aggregation on parties

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
insert {
    graph <graph/aggregated-results> {
    ?election myd:vote ?party ; myp:vote ?VOTE_URI .
    ?VOTE_URI a my:ElectionVote ;
        myps:vote ?party ;
    	mypq:valid_votes_recieved ?sum_valid_votes ;
        mypq:invalid_votes_recieved ?sum_invalid_votes ;
    .
    }
} 
where {
{select ?election ?party (sum(?valid_votes) as ?sum_valid_votes) (sum(?invalid_votes) as ?sum_invalid_votes) 
    where {
        ?party a my:LocalParty ;
              #myd:candidacy ?election ;
              rdfs:label ?name .
        ?voting myp:vote ?vote  ;
                myd:election ?election .
        ?vote myps:vote ?party;
            mypq:valid_votes_recieved ?valid_votes ;
            mypq:invalid_votes_recieved ?invalid_votes .
     } 
group by ?election ?party }
	bind(uri(concat("vote/",strafter(str(?election),str(election:)),"/",strafter(str(?party),str(party:)))) as ?VOTE_URI)        
}
```

# Integration Queries 

Wikidata Municipalities and Oblast queries. 
Not working need to debug > produces static mapping which is ok for now. 


```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
	?s a my:Municipality ;
	    rdfs:label ?munLabel ; 
	    myd:mir ?MIRURI ; 
	    myd:province ?obl ; 
	    geo:hasGeometry ?MUN_GEO ; 
	    myd:wdid ?mun .
    ?obl a my:Province ; rdfs:label ?oblLabel .
    ?MUN_GEO a geo:Geometry ; geo:asWKT ?munCoord .        
}
where { 
	?s a my:Municipality ; myd:wdid ?mun .
    service <https://query.wikidata.org/sparql> {
        ?mun wdt:P625 ?munCoord .
        ?mun wdt:P131?/wdt:P7938 ?mir ; wdt:P131 ?obl .
        ?mir p:P31/pq:P1545 ?mirnum ; wdt:P625 ?mirCoord .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg,en". 
            ?mun rdfs:label ?munLabel .
            ?mir rdfs:label ?mirLabel .
            ?obl rdfs:label ?oblLabel .
        }     
    }
    bind(uri(concat(str(jurisdiction:),?mirnum)) as ?MIRURI)
    bind(uri(concat(str(?s),"/geo")) as ?MUN_GEO)
    bind(uri(concat(str(?MIRURI),"/geo")) as ?MIR_GEO)
} 
```

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
	?MIRURI a my:MIR ; rdfs:label ?mirLabel ; geo:hasGeometry ?MIR_GEO ; myd:wdid ?mir ; myd:number ?mirnum .
    ?MIR_GEO a geo:Geometry ; geo:asWKT ?mirCoord .  
}
where { 
    service <https://query.wikidata.org/sparql> {
        ?mir wdt:P31 wd:Q43791141 ; p:P31/pq:P1545 ?mirnum ; wdt:P625 ?mirCoord .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg,en". 
            ?mir rdfs:label ?mirLabel .
        }     
    }
    bind(uri(concat(str(jurisdiction:),?mirnum)) as ?MIRURI)
    bind(uri(concat(str(?s),"/geo")) as ?MUN_GEO)
    bind(uri(concat(str(?MIRURI),"/geo")) as ?MIR_GEO)
}
```

Places from Wikdata

```sparql 
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX place: <https://elections.ontotext.com/resource/place/> 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
    ?PLACE_URI a my:Place ;
               rdfs:label ?placeLabel ;
               myd:municipality ?s ;
               geo:hasGeometry ?PLACE_GEO_URI ;
               myd:idwd ?place ;
    .
    ?PLACE_GEO_URI a geo:Geometry ; geo:asWKT ?placeCoord . 
} where { 
	?s myd:wdid ?mun
    service <https://query.wikidata.org/sparql> {
        ?place wdt:P131 ?mun ; p:P3990 ?ekst ; wdt:P625 ?placeCoord .
        ?ekst ps:P3990 ?ekatte .
        filter not exists {?ekst pq:P518 [] }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg". 
            ?place rdfs:label ?placeLabel .
        }
    bind(uri(concat(str(place:),?ekatte)) as ?PLACE_URI)
    bind(uri(concat(str(place:),?ekatte,"/geo")) as ?PLACE_GEO_URI)   
    }
}
```
### Create metasections based on sections with matching ID

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
graph <graph/metasections> {	
	?metasec a my:MetaSection .
    ?sec  myd:meta_section ?metasec .    
}}
where {
    ?sec a my:Section ; myd:number ?num .
    bind(uri(concat("metaSection/",?num)) as ?metasec)
}
```