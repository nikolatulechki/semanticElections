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
