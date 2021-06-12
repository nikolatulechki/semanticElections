# AKF Data analysis queries and notes

## Queries 

### Data export 

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX metaSection: <https://elections.ontotext.com/resource/metaSection/>
select ?election_id ?sec_id ?risky ?voters_registered ?voters_voted ?votes_invalid ?turnover ?winner_votes ?winner_ratio ?winner_label  {
    ?v myp:vote ?vs ;
       myd:voters_voted_count ?voters_voted ; 
       myd:voters_count ?voters_registered ; 
#       myd:voters_additional_count ?voters_additional ; #todo should fix for pi2013
       myd:votes_invalid_count ?votes_invalid ;
       myd:main_election ?main_election ;
     . 
    ?vs mypq:valid_votes_recieved ?winner_votes ;
        myps:vote ?local_party ;
    .
    bind(?winner_votes/?voters_voted as ?winner_ratio)
    bind(?voters_voted/?voters_registered as ?turnover)
    
    bind(strafter(str(?ms),str(metaSection:)) as ?sec_id)
    bind(strafter(str(?main_election),str(election:)) as ?election_id)
    
    ?local_party rdfs:label ?local_party_label .
    optional {             
        ?local_party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_party_label .
    }
    bind(coalesce(?main_party_label,?local_party_label) as ?winner_label)
    {
        select ?ms ?risky ?v (max(?vv) as ?winner_votes) {
            ?v a my:Voting ;
               myd:section/myd:meta_section ?ms ;
                          myp:vote/mypq:valid_votes_recieved ?vv 
            #filter(?vv > 100)
            filter(contains(str(?v),"pi"))
            {
                select ?ms ?risky where {
                    ?ms a my:MetaSection ;
                        optional{
                        ?ms myd:is_risky ?risky 
                    } 
                    filter exists {
                        election:pi2017 ^myd:main_election/myd:meta_section ?ms 
                    }
                } 
                #limit 200
            }
        } group by ?ms ?risky ?v 
    }
} order by ?sec_id ?election_id
```

## Anomalous sections

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select ?election_id ?sec_id ?mun_label ?party_label ?total_votes_sec ?sec_party_votes ?sec_party_vote_ratio ?mun_party_votes_total ?mun_party_vote_ratio ?prot_link ?pdf_link {
    ?sec a  my:Section ;
         myd:number ?sec_id ;
         myd:place/myd:municipality ?mun ;
                  myd:main_election ?election;
                  .
    bind(strafter(str(?election),str(election:)) as ?election_id)
    optional{?sec myd:meta_section/myd:isRisky ?risky }
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
            myd:main_election ?election ;
            myd:link_html ?prot_link ;
            myd:link_pdf ?pdf_link ;
            .
    ?vote_st myps:vote ?party ;
             #             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?sec_party_votes ;
             .
    ?party rdfs:label ?party_label .
    ?mun rdfs:label ?mun_label .
    bind(floor((?sec_party_votes/?total_votes_sec)*10000)/100 as ?sec_party_vote_ratio)
    filter(?sec_party_votes > 100)
    filter(?sec_party_vote_ratio/?mun_party_vote_ratio > 2)    
    {
        select ?election ?mun ?party (sum(?valid_votes) as ?mun_party_votes_total) (floor((sum(?valid_votes)/sum(?total_votes))*10000)/100 as ?mun_party_vote_ratio)
        where {
            #    bind(<election/mi2019/os> as ?el_filter) # Местни Избори 2019 ОС
            values ?election {
                <election/pi2013>
                <election/pi2014>
                <election/pi2017>
            }
            #   bind(<election/pi2017> as ?election) # Парламент 2017
            #   bind(jurisdiction:2246 as ?mun) # Столична община
            #   bind(jurisdiction:2105 as ?mun) # община Борино
            #   bind(jurisdiction:1539 as ?mun) # община Кнежа 
            ?party a my:LocalParty ;
                   #myd:candidacy ?election ;
                   rdfs:label ?partyName .
            ?voting myp:vote ?vote  ;
                    myd:main_election ?election;
                    myd:votes_valid_count ?total_votes ;
                    myd:section/myd:place/myd:municipality ?mun ;
                                         .
            ?vote myps:vote ?party;
                  mypq:valid_votes_recieved ?valid_votes ;
                  .
        } 
        group by ?election ?mun ?party order by ?sec_id ?election_id
    }
} 
```

## Anomalous sections arcGIS output

Map URL <https://www.arcgis.com/apps/StorytellingSwipe/index.html?appid=0ccfb76657c64a36b37c6062a5e20090>

Story URL <https://arcg.is/1W0jXG>

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
select 
?sec_id ?winner_label ?lat ?lon ?sec_party_votes ?sec_party_vote_ratio ?prot_link ?section_label ?mun_party_votes_total ?mun_party_vote_ratio ?sec_mun_party_ratio ?mun_label
#?sec_id ?mun_label ?party_label ?total_votes_sec ?sec_party_votes ?sec_party_vote_ratio ?mun_party_votes_total ?mun_party_vote_ratio ?prot_link ?pdf_link 

{
    ?sec a  my:Section ;
         rdfs:label ?section_label ;
         myd:number ?sec_id ;
         myd:place/myd:municipality ?mun ;
                  myd:main_election ?election;
                  .
    ?mun rdfs:label ?mun_label .
    filter(lang(?mun_label)="bg")
    bind(strafter(str(?election),str(election:)) as ?election_id)
    optional{?sec myd:meta_section/myd:isRisky ?risky }

    {?sec myd:votingPlace ?place} 
     UNION 
    {?sec myd:place ?place 
        filter not exists{?sec myd:votingPlace []}
    }
    ?place geo:hasGeometry
            ?geo .
    ?geo geo:lat ?lat ; geo:long ?lon .
    
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
            myd:main_election ?election ;
            myd:link_html ?prot_link ;
            myd:link_pdf ?pdf_link ;
            .
    ?vote_st myps:vote ?party ;
             #             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?sec_party_votes ;
             .
    ?party rdfs:label ?party_label .
        optional {             
        ?party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_party_label .
    }
    bind(coalesce(?main_party_label,?party_label) as ?winner_label)
    
    ?mun rdfs:label ?mun_label .
    bind(floor((?sec_party_votes/?total_votes_sec)*10000)/100 as ?sec_party_vote_ratio)
    bind(floor((?sec_party_votes/?mun_party_votes_total)*10000)/100 as ?sec_mun_party_ratio) 
    filter(?sec_party_votes > 100)
    filter(?sec_party_vote_ratio/?mun_party_vote_ratio > 2)    
    {
        select ?election ?mun ?party (sum(?valid_votes) as ?mun_party_votes_total) (floor((sum(?valid_votes)/sum(?total_votes))*10000)/100 as ?mun_party_vote_ratio)
        where {
            #    bind(<election/mi2019/os> as ?el_filter) # Местни Избори 2019 ОС
#            values ?election {
#                <election/pi2013>
#                <election/pi2014>
#                <election/pi2017>
#            }
                bind(<election/pi2017> as ?election) # Парламент 2017
#           #    bind(jurisdiction:2246 as ?mun) # Столична община
            #   bind(jurisdiction:2105 as ?mun) # община Борино
            #   bind(jurisdiction:1539 as ?mun) # община Кнежа 
            ?party a my:LocalParty ;
                   #myd:candidacy ?election ;
                   rdfs:label ?partyName .
            ?voting myp:vote ?vote  ;
                    myd:main_election ?election;
                    myd:votes_valid_count ?total_votes ;
                    myd:section/myd:place/myd:municipality ?mun ;
                                         .
            ?vote myps:vote ?party;
                  mypq:valid_votes_recieved ?valid_votes ;
                  .
        } 
        group by ?election ?mun ?party order by ?sec_id ?election_id
    }
}
```


## Entropy section ARCgis Output

STORY url <https://arcg.is/0zKq5X>

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
select 
?sec_id ?winner_label ?lat ?lon ?winner_votes ?winner_vote_ratio  ?prot_link ?section_label ?ENTROPY
#?sec_id ?mun_label ?party_label ?total_votes_sec ?sec_party_votes ?sec_party_vote_ratio ?mun_party_votes_total ?mun_party_vote_ratio ?prot_link ?pdf_link 

{
    ?sec a  my:Section ;
         rdfs:label ?section_label ;
         myd:number ?sec_id ;
         myd:place/myd:municipality ?mun ;
                  myd:main_election ?election;
                  .
    ?mun rdfs:label ?mun_label .
    filter(lang(?mun_label)="bg")
    bind(strafter(str(?election),str(election:)) as ?election_id)
    optional{?sec myd:meta_section/myd:isRisky ?risky }

    {?sec myd:votingPlace ?place} 
     UNION 
    {?sec myd:place ?place 
        filter not exists{?sec myd:votingPlace []}
    }
    ?place geo:hasGeometry
            ?geo .
    ?geo geo:lat ?lat ; geo:long ?lon .
    
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
            myd:main_election ?election ;
            myd:link_html ?prot_link ;
            myd:link_pdf ?pdf_link ;
            myd:entropy ?entropy 
            .
    filter(?entropy < 0.8)
    bind(strdt(str(?entropy),xsd:decimal) as ?ENTROPY)
    ?vote_st myps:vote ?party ;
             #             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?winner_votes ;
             .
    ?party rdfs:label ?party_label .
     optional {             
        ?party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_party_label .
    }
    bind(coalesce(?main_party_label,?party_label) as ?winner_label)
    
    ?mun rdfs:label ?mun_label .
    bind(floor((?winner_votes/?total_votes_sec)*10000)/100 as ?winner_vote_ratio)

    {
        select ?voting (max(?valid_votes) as ?winner_votes)
        where {
            #    bind(<election/mi2019/os> as ?el_filter) # Местни Избори 2019 ОС
#            values ?election {
#                <election/pi2013>
#                <election/pi2014>
#                <election/pi2017>
#            }
#              bind(<election/pi2017> as ?election) # Парламент 2017
#              bind(<election/pi2017> as ?election) # Парламент 2017
#               bind(jurisdiction:2246 as ?mun) # Столична община
            #   bind(jurisdiction:2105 as ?mun) # община Борино
            #   bind(jurisdiction:1539 as ?mun) # община Кнежа 
            ?party a my:LocalParty ;
                   #myd:candidacy ?election ;
                   rdfs:label ?partyName .
            ?voting myp:vote ?vote  ;
                    myd:election ?el ;
                    myd:main_election ?election;
                    myd:votes_valid_count ?total_votes ;
                    myd:section/myd:place/myd:municipality ?mun ;
            .
            filter(contains(str(?el),"mi2015/ko/tur1"))
            filter(?total_votes > 100)
            ?vote myps:vote ?party;
                  mypq:valid_votes_recieved ?valid_votes ;
                  .
        } 
        group by ?voting 
    }
}
```

## Risky sections arc gis dump

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
select ?section_label ?sec_id ?mun_label ?city_label ?lat ?lon ?total_votes_sec ?winner_votes ?winner_vote_ratio ?winner_label ?link_html ?link_pdf ?models ?n_models ?gplace_link ?gcoords_link {
    
    ?sec a  my:Section ;
         rdfs:label ?section_label ;
         myd:number ?sec_id ;
         myd:place ?city .
    ?city myd:municipality ?mun ;
          rdfs:label ?city_label ;
	.
    ?mun rdfs:label ?mun_label .
    filter(lang(?mun_label)="bg")
    filter(lang(?city_label)="bg")
    bind(strafter(str(?election),str(election:)) as ?election_id)
    
    {?sec myd:votingPlace ?place} 
     UNION 
    {?sec myd:place ?place 
        filter not exists{?sec myd:votingPlace []}
    }
    ?place geo:hasGeometry
            ?geo .
    ?geo geo:lat ?lat ; geo:long ?lon .
    optional{
		?place geo:hasGeometry/myd:source "google_maps" .
        bind(uri(concat("https://www.google.com/maps/place/?q=place_id:",strafter(str(?place),str(<votingPlace/>)))) as ?gplace_link)                                                  
    }
    optional{
		?place geo:hasGeometry/myd:source "parent_place_coords" .
        bind(uri(concat("https://www.google.com/maps/search/?api=1&query=",str(?lat),",",str(?lon))) as ?gcoords_link)                                                  
    }
   
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
            myd:main_election ?election ;
            myd:link_html ?link_html ;
            myd:link_pdf ?link_pdf ;
            .
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?winner_votes .
    bind(floor((?winner_votes/?total_votes_sec)*10000)/100 as ?winner_vote_ratio)
 	
    ?party rdfs:label ?party_label .
     optional {             
        ?party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_party_label .
    }
    bind(coalesce(?main_party_label,?party_label) as ?winner_label)
    
    {
        select ?voting (max(?valid_votes) as ?winner_votes) (count(distinct ?model) as ?n_models) (group_concat(distinct ?model;separator="|") as ?models) where {
            bind(<election/pi2017> as ?election) # Парламент 2017 
            ?sec a  my:Section ;
                 myd:meta_section ?ms .
            ?ms myd:isRisky true ;
                myd:risky_model ?model .
            ?voting myp:vote ?vote  ;
                    myd:main_election ?election ;
                    myd:section ?sec .
            ?vote myps:vote ?party;
                  mypq:valid_votes_recieved ?valid_votes ;
                  } group by ?voting 
    }
}
```

## Gis Export 1 party votes

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
select ?place ?section_label ?sec_id ?mun_label ?city_label ?lat ?lon ?total_votes_sec ?winner_votes ?winner_vote_ratio ?winner_label ?link_html ?link_pdf ?models ?n_models ?gplace_link ?gcoords_link {
    
    
    ?sec a  my:Section ;
         rdfs:label ?section_label ;
         myd:number ?sec_id ;
         myd:place ?city .
    ?city myd:municipality ?mun ;
          rdfs:label ?city_label ;
	.
    ?mun rdfs:label ?mun_label .
    filter(lang(?mun_label)="bg")
    filter(lang(?city_label)="bg")
    bind(strafter(str(?election),str(election:)) as ?election_id)
    
    {?sec myd:votingPlace ?place} 
     UNION 
    {?sec myd:place ?place 
        filter not exists{?sec myd:votingPlace []}
    }
    ?place geo:hasGeometry
            ?geo .
    ?geo geo:lat ?lat ; geo:long ?lon .
    optional{
		?place geo:hasGeometry/myd:source "google_maps" .
        bind(uri(concat("https://www.google.com/maps/place/?q=place_id:",strafter(str(?place),str(<votingPlace/>)))) as ?gplace_link)                                                  
    }
    optional{
		?place geo:hasGeometry/myd:source "parent_place_coords" .
        bind(uri(concat("https://www.google.com/maps/search/?api=1&query=",str(?lat),",",str(?lon))) as ?gcoords_link)                                                  
    }
   
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
            myd:main_election ?election ;
            myd:link_html ?link_html ;
            myd:link_pdf ?link_pdf ;
            .
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?winner_votes .
    bind(floor((?winner_votes/?total_votes_sec)*10000)/100 as ?winner_vote_ratio)
 	
    ?party rdfs:label ?party_label .
     optional {             
        ?party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_party_label .
    }
    bind(coalesce(?main_party_label,?party_label) as ?winner_label)
    
    {
        select ?voting (max(?valid_votes) as ?winner_votes) (count(distinct ?model) as ?n_models) (group_concat(distinct ?model;separator="|") as ?models) where {
            bind(<election/pi2014> as ?election) # Парламент 2017 
            ?sec a  my:Section ;
                 myd:meta_section ?ms .
            ?ms myd:isRisky true ;
                myd:risky_model ?model .
            ?voting myp:vote ?vote  ;
                    myd:main_election ?election ;
                    myd:section ?sec .
            ?vote myps:vote ?party;
                  mypq:valid_votes_recieved ?valid_votes ;
                  } group by ?voting having(?n_models = 1)
    }
}
```

### Volya vs BBC 

Comparing sections with small number of votes with others

party | total < 20 | count < 20 | total > 20 | count > 20 
------|------------|------------|------------|------------
volya |   79516    |   9068     |   67462    |    2095
bbc   |   72983    |   7990     |   107740   |    3286

### Risky Aggregate Data

```spaqrl
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?party_label (sum(?votes) as ?sum_votes) (avg(?party_ratio) as ?avg_ratio)  where { 
	?v a my:Voting ;
    	 myd:section/myd:meta_section/myd:isRisky true ;
         myd:main_election election:pi2017 ; #ELECTION HERE
         myd:vote ?party ;
         myp:vote ?vs ;
         myd:voters_voted_count ?voters ;
    .
    ?vs myps:vote ?party ;
        mypq:valid_votes_recieved ?votes ;
    .
    bind(?votes/?voters as ?party_ratio)
    ?party myd:party ?main_party .
    ?main_party rdfs:label ?party_label .
} group by ?party_label order by desc(?sum_votes)
```

2014 vs 2017
1.32 entropy in risky
1.71 avg entropy in non-risky 

```sparql 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
insert {
    graph graph:risky_low_entropy {
        ?ms myd:isRisky true 
    }}
WHERE        {
        select ?ms (avg(?ent) as ?ent_avg) where {
        ?v a my:Voting ;
        #    	 myd:section/myd:meta_section/myd:isRisky true ;
        myd:main_election ?main_el ;
        #election:pi2017 ; #ELECTION HERE
        myd:entropy ?ent ;
        myd:voters_voted_count ?voters ;
        myd:section/myd:meta_section ?ms ;
        .
        filter(contains(str(?main_el),"pi"))
        #    filter(?ent < 1.1)
        filter(?voters > 100)
        #    filter not exists {?v myd:section/myd:meta_section/myd:isRisky true ;}
} group by ?ms having(?ent_avg < 1) 
}
```

 ## Dolni Cibar

Избирателна активност 

```spaqrl
# Агрегирани резултати по населено място 

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select ?place_label ?date ?el ?el_label (sum(?voters) as ?sum_voters) (sum(?voted) as ?sum_voted) where {
    
    bind(place:22530 as ?place) # place:EKATTE 
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el .
    ?voting myd:section ?sec ;
            myd:voters_voted_count ?voted ;
            myd:voters_count ?voters .
    ?el rdfs:label ?el_label ; myd:date ?date . 
    ?place rdfs:label ?place_label .
} group by ?date ?place_label ?el ?el_label  order by ?date ?el 
```

Разбивка

```sparql
# Агрегирани резултати по населено място 

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select ?place_label ?date ?el ?el_label ?party_label (sum(?n_votes) as ?sum_votes) where {
    
    bind(place:22530 as ?place) # place:EKATTE 
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el .
    ?voting myd:section ?sec ;
            myp:vote ?vote_st .
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?n_votes.
    ?party rdfs:label ?party_label .
    ?el rdfs:label ?el_label ; myd:date ?date . 
    ?place rdfs:label ?place_label .
} group by ?date ?place_label ?el ?el_label ?party_label order by ?date ?el desc(?sum_votes)
```

```sparql
PREFIX place: <http://edu.ontotext.com/resource/place/>
PREFIX : <http://edu.ontotext.com/resource/ontology/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX ethnic_group: <http://edu.ontotext.com/resource/ethnic_group/>
select * where { 
    bind(place:Q391159 as ?place_edu)
    ?obs :place ?place_edu ; qb:dataSet <http://edu.ontotext.com/resource/cube/nsi_ethnicity/2011> ;
    	 :ethnic_group ?eg ;
      	 :quantity_people ?qp ;
    bind(if(sameterm(?eg,ethnic_group:roma),?qp,0) as ?roma)
    bind(if(sameterm(?eg,ethnic_group:bg),?qp,0) as ?bg)
    bind(if(sameterm(?eg,ethnic_group:tr),?qp,0) as ?tr)
} limit 100 
```

### Crazy federated query for ethnicity

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX place: <http://edu.ontotext.com/resource/place/>
PREFIX : <http://edu.ontotext.com/resource/ontology/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX ethnic_group: <http://edu.ontotext.com/resource/ethnic_group/>

select ?sec_id ?risky ?place_label ?ekatte ?BG ?TR ?ROMA ?TOTAL where { 
	?ms a my:MetaSection .
    optional{?ms myd:isRisky ?risky}
    ?sec myd:meta_section ?ms ; 
         myd:place ?place ;
    	 myd:number ?sec_id .
    ?place rdfs:label ?place_label .
    bind(strafter(str(?place),"https://elections.ontotext.com/resource/place/") as ?ekatte)
    filter(contains(str(?sec),"pi2017"))
    {select ?place (sum(?roma) as ?ROMA) (sum(?tr) as ?TR) (sum(?bg) as ?BG) (sum(?qp) as ?TOTAL) {
    ?place a my:Place ; rdfs:label ?place_label ; myd:wikidata_entity ?wd . 
    bind(uri(replace(str(?wd),str(wd:),str(place:))) as ?place_edu)
    service <http://edu.ontotext.com/repositories/semantic-schools> {
         ?obs :place ?place_edu ; qb:dataSet <http://edu.ontotext.com/resource/cube/nsi_ethnicity/2011> ;
    	 :ethnic_group ?eg ;
      	 :quantity_people ?qp ;
        bind(if(sameterm(?eg,ethnic_group:roma),?qp,0) as ?roma)
        bind(if(sameterm(?eg,ethnic_group:bg),?qp,0) as ?bg)
        bind(if(sameterm(?eg,ethnic_group:tr),?qp,0) as ?tr)
    }} group by ?place}
} 

```

#Ethnic group query on EDU
```spqrql
PREFIX place: <http://edu.ontotext.com/resource/place/>
PREFIX : <http://edu.ontotext.com/resource/ontology/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX ethnic_group: <http://edu.ontotext.com/resource/ethnic_group/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?label ?eg ?qp where { 
    bind(place:Q407207 as ?place_edu)
    ?obs :place ?place_edu ; qb:dataSet <http://edu.ontotext.com/resource/cube/nsi_ethnicity/2011> ;
    	 :ethnic_group ?eg ;
      	 :quantity_people ?qp ;
    .    
    ?place_edu rdfs:label ?label .   
    filter(lang(?label)="bg")
    bind(if(sameterm(?eg,ethnic_group:roma),?qp,0) as ?roma)
    bind(if(sameterm(?eg,ethnic_group:bg),?qp,0) as ?bg)
    bind(if(sameterm(?eg,ethnic_group:tr),?qp,0) as ?tr)
} limit 100 
```