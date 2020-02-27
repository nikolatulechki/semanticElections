# Example SPARQL queries


### Всички кандидати на дадена партия

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
select ?cand ?election ?name ?elLabel ?round {
    ?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents <party/66> .
    ?election rdfs:label ?elLabel .
    optional {?election myd:round ?round .}
}
```

### Candidates on tur 1 with aggregated votes on municipality level 

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
select ?election ?party ?cand ?name (sum(?votes) as ?sum_votes)
where { 
#bind(<https://github.com/nikolatulechki/semanticElections/resource/entity/election/mi2019/ko/0101/tur1> as ?election)
?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents ?party .
?election myd:round 1 .
?voting myd:partOf ?election . 
?s ^myp:vote ?voting ; myps:vote ?party ; mypq:valid_votes_recieved ?votes .     
} group by ?election ?party ?cand ?name order by desc(?sum_votes)
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

## Postprocessing queries 

Query to clean-up broken labels 
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

fix double party types +

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

Gen Coalitions (temp)

```sparql
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
select 

?party ?municipality ?name (group_concat(distinct ?el_notation;separator=";") as ?elections) 
where { 
    ?party a my:Party ; 
        myd:type "independant" ; 
        rdfs:label ?name ;
        ^mypq:represents/myps:candidacy ?cand ;
    .
    ?cand myd:municipality/rdfs:label ?municipality ; myd:partOf ?election .
    bind(strafter(str(?election),concat(str(my:),"election/mi2019/")) as ?el_notation) 
    
} 
group by ?party ?municipality ?name 
```

### Candidate Matching query 

Insert does not wqork with gdb 9. Bets result is with constrct and then imprting th .ttl file. 

```
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mys: <https://github.com/nikolatulechki/semanticElections/resource/entity/statement/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
construct {
    ?c1 owl:sameAs ?c2 .
}
where { 
    ?c1 a my:Candidate ; rdfs:label ?l1 .
    ?c2 a my:Candidate ; rdfs:label ?l1 .
    filter(!sameterm(?c1,?c2))
    ?c1 myp:candidacy ?cy1 .
    ?c2 myp:candidacy ?cy2 .
    ?cy1 myps:candidacy/myd:partOf?/myd:municipality/^myd:municipality/^myd:partOf?/^myps:candidacy ?cy2 .
    ?cy1 mypq:represents/^mypq:represents ?cy2 .
} 
```

Names not following the main pattern 
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

Election retromatching
```
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
insert {
    ?e myd:wdMatch ?wd .
}
where { 
    ?e a my:Election ; myd:partOf <election/mi2019/ko> ; myd:municipality/myd:wdMatch ?mun .
    service <https://query.wikidata.org/sparql> {
        ?wd wdt:P31 wd:Q69463245 ; wdt:P1001 ?mun .
    }                  
} 
```

```spaqrl
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

select * where { 
    ?e a my:Election ; myd:partOf <election/mi2019/ko> ; myd:wdMatch ?wd .
    ?vr myd:partOf ?e ; rdfs:label ?vlabel ; myd:round 1 .
    service <https://query.wikidata.org/sparql> {
          SERVICE wikibase:label {
            bd:serviceParam wikibase:language "bg" .
            ?wd rdfs:label ?bgLabel .
          }
          SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en" .
            ?wd rdfs:label ?enLabel .
          }
    }
    bind(concat(?bgLabel," - Първи тур") as ?roundLabelBg)
    bind(concat("First round of ",?enLabel) as ?roundLabelEn)
    
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

## Aggregation Queries

Local elections - aggregation on candidates

!!! Fucked up - One candidacy for both rounds - need separate ones :( fix this 

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
PREFIX onto: <http://www.ontotext.com/>
construct {
#    graph my:graph-ko-aggregate-results { 
    ?csy mypq:valid_votes_recieved ?sum_valid_votes ;
         mypq:invalid_votes_recieved ?sum_invalid_votes ;
     .
#    }
}
#from onto:disable-sameAs
where
{
    select ?election ?csy (sum(?valid_votes) as ?sum_valid_votes) (sum(?invalid_votes) as ?sum_invalid_votes) 
    where {
        ?cand a my:Candidate ;
              myd:candidacy ?election ;
              rdfs:label ?name ;
              myp:candidacy ?csy .
        ?csy  mypq:represents ?party .
        ?voting myd:partOf ?election .
        ?s ^myp:vote ?voting ;
            myps:vote ?party ;
            mypq:valid_votes_recieved ?valid_votes ;
            mypq:invalid_votes_recieved ?invalid_votes .
        ?election myd:round [] .		       
    } 
    group by ?election ?csy 
}
```