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