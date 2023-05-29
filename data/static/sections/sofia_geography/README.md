# Geography of Sofia stations

- Based on a set of polygons from 2020-03-19 
- Assuming these correspond to mi2019 stations

https://ge.sofiaplan.bg/

https://api.triplydb.com/s/Idy7BnEfc

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX wd: <http://www.wikidata.org/entity/>
select * {
{select ?ge ?ge_geo ?ge_geoTooltip ?party_label     
(SUM(?voters) as ?VOTERS_GE)     
(SUM(?VOTED) as ?VOTED_GE) 
(SUM(?PARTY_VOTES) as ?PARTY_VOTES_GE) 
(?PARTY_VOTES_GE/?VOTED_GE as ?PARTY_RATIO)
(concat("jet,",str(?PARTY_RATIO*2)) as ?ge_geoColor) where {
    
#    bind(wd:Q133968 as ?party) #GERB
    bind(wd:Q108601789 as ?party) #PP
#    bind(wd:Q28943121 as ?party) #VUZ
#    bind(wd:Q62808154 as ?party) #DB
    ?ge a my:Neighborhood ;
        rdfs:label ?ge_geoTooltip ;
        geo:hasGeometry/geo:asWKT ?ge_geo ;
    .
    ?mi_sec myd:neighborhood ?ge ; myp:neighborhood ?st .
    ?st mypq:inclusion_ratio ?ratio ; myps:neighborhood ?ge .
    
    ?voting a my:Voting ; myd:main_election election:pi2022 ; 
              myd:section/myd:matched_section/myd:section ?mi_sec ; 
              myd:voters_voted_count ?voted ;
              myd:voters_count ?voters .
    
    bind(floor(?voted*?ratio) as ?VOTED)
    
    ?voting myp:vote ?vs .
    ?vs mypq:valid_votes_recieved ?party_votes ; 
        myps:vote/myd:party/myd:party ?party  . 
    ?party rdfs:label ?party_label .
    bind(floor(?party_votes*?ratio) as ?PARTY_VOTES)
    } group by ?ge ?ge_geo ?ge_geoTooltip ?party_label }

  bind(concat(
     "GE: ",?ge_geoTooltip,"\n",
     "Party: ",?party_label,"\n",
     "Voted: ",str(?VOTED_GE),"\n",
     "Voters: ",str(?VOTERS_GE),"\n",      
     "Party_votes: ",str(?PARTY_VOTES_GE),"\n",
     "Party Ratio: ",str(?PARTY_RATIO)
  ) as ?ge_geoLabel)  
}
```
## Show sections form one cycle in YasGUI

```sparql
BASE  <https://elections.ontotext.com/resource/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
select distinct ?sec ?SECTION ?SECTIONColor  where {
  values (?election ?SECTIONColor) {
#    (election:pi2022 "red")
    (election:pi2023 "blue")

}
            ?sec a my:Section ; myd:main_election ?election; geo:hasGeometry/geo:asWKT ?SECTION .
        }
```

## Low inclusion rations on yas

```
BASE  <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>


select distinct ?sec ?SECTION ("red" as ?SECTIONColor)  ?CAND  where {


  ?sec a my:Section ; myd:main_election ?election; geo:hasGeometry/geo:asWKT ?SECTION . 
  ?cand geo:hasGeometry/geo:asWKT ?CAND .
    
      ?sec a my:Section ; myd:main_election election:pi2023 ; myp:geo_match [myps:geo_match ?cand ; mypq:inclusion_ratio ?ratio ] .
            filter(?ratio < 0.50 && ?ratio > 0.30 )
}
```


### Compare sections with and without geography 

```sparql 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
select 
?el 
(count(distinct ?sec) as ?section_count)
(count(distinct ?sec_g) as ?section_geo_count)
(sum(?voted) as ?sum_voted)
(sum(?voted_g) as ?sum_voted_g)
(?sum_voted - ?sum_voted_g as ?dif_voted)
where {
    {
        ?sec a my:Section ;
             myd:place/myd:municipality jurisdiction:2246 ;
             myd:main_election ?el .
        ?v a my:Voting ;
             myd:section ?sec ;
             myd:voters_voted_count ?voted .
    } UNION {
        ?sec_g a my:Section ;
             myd:place/myd:municipality jurisdiction:2246 ;
             myd:main_election ?el ;
             geo:hasGeometry [].
        ?v_g a my:Voting ;
             myd:section ?sec_g ;
             myd:voters_voted_count ?voted_g .
    }
} group by ?el order by ?el
```
### Sections w/o geography

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
        ?sec a my:Section ;
             rdfs:label ?sec_label ;
             myd:place/myd:municipality jurisdiction:2246 ;
             myd:main_election election:pi2023 ;
    		 myd:streetAddress ?addr .
    ?v myd:section ?sec ; myd:voters_voted_count ?voted .
    filter not exists {?sec geo:hasGeometry []}
} limit 100 
```
GE-District missmatch
Step 1-assign District to GE
Step 2 sections should not be related to ge outside district  