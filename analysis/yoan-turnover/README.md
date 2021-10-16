[gfolder](https://drive.google.com/drive/u/1/folders/1TNcxQumf1vCljnDNv2_0D_rO5U4RmTFG)

# Very high winner rate

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
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX wd: <http://www.wikidata.org/entity/>
#select ?v ?voting_label ?vote_party ?voters_voted ?section_label ?election_party_label ?vote_ratio_party ?voter_turnover ?protocol 
select *
where { 
              
    ?election_party rdfs:label ?election_party_label
    
    {select ?v ?election_party {
        ?v myp:vote ?vote .
        ?vote mypq:valid_votes_recieved ?max_votes ;
          myps:vote ?election_party ;  
         .
        {select ?v (max(?votes) as ?max_votes) {
            bind(election:pi2021 as ?main_election) #use ?main_election for local and parliamentary 
            ?election myd:main_election ?main_election . #uncomment for local and parliamentary 
            ?v a my:Voting ; myd:election ?election ; myp:vote/mypq:valid_votes_recieved ?votes            
        } group by ?v }  
    }}
    
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:election ?election ;
        myd:voters_count ?voters_listed ;
        myd:voters_voted_count ?voters_voted ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section ?section ;
        myd:link_html ?protocol ;         
    .
    ?section myd:number ?sec_id ; 
             myd:place/rdfs:label ?place ;
             myd:place/myd:municipality/rdfs:label ?mun ;
             myd:place/myd:municipality/myd:province/rdfs:label ?obl ;
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          myps:vote ?election_party ;                      
    .
    filter(?voters_voted > 50)
    bind(floor((?vote_party/?voters_voted)*10000)/100 as ?vote_ratio_party)
    bind(floor((?voters_voted/?voters_listed)*10000)/100 as ?voter_turnover)    
    filter(?vote_ratio_party >= 70)
}
```

# Turnover Compare across sections

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select * where {
    ?v4 a my:Voting ;
    myd:election/myd:main_election election:pi2021 ;
                    myd:voters_count ?voters_listed_4 ;
                    myd:voters_voted_count ?voters_voted_4 ;
                    myd:section ?section_4 ;
                    myd:link_html ?protocol_4 ;
    .
    ?section_4 myd:number ?sec_id ;
               myd:place ?place .
    ?place rdfs:label ?place_label ;
           myd:municipality/rdfs:label ?mun ;
           myd:municipality/myd:province/rdfs:label ?obl ;
                                                        .
    filter(?voters_voted_4 > 50)
    bind(?voters_voted_4/?voters_listed_4 as ?voter_turnover_4)    
    ?v7 a my:Voting ;
    myd:election/myd:main_election election:pi2021_07 ;
                    myd:voters_count ?voters_listed_7 ;
                    myd:voters_voted_count ?voters_voted_7 ;
                    myd:section ?section_7 ;
                    myd:link_html ?protocol_7 ;
    .
    ?section_7 myd:place ?place ; myd:meta_section/^myd:meta_section ?section_4
    filter(?voters_voted_7 > 50)
    bind(?voters_voted_7/?voters_listed_7 as ?voter_turnover_7)
    bind(?voter_turnover_7-?voter_turnover_4 as ?turnover_delta)
    filter(abs(?turnover_delta) > 0.10)
} 
```

## Different winners in sections

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
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX wd: <http://www.wikidata.org/entity/>

select ?obl ?mun ?place_label ?sec_id ?main_party_label_4 ?main_party_label_7 ?voters_listed_4 ?voters_voted_4 ?vote_party_4 ?voters_listed_7 ?vote_ratio_party_4 ?voter_turnover_4 ?voters_listed_7 ?voters_voted_7 ?vote_party_7 ?vote_ratio_party_7 ?vote_party_7_loser ?vote_ratio_party_7_loser ?voter_turnover_7 (?vote_party_7_loser-?vote_party_4 as ?delta_loser) ?protocol_4 ?protocol_7
#select *
where {
    {
        select ?v_7 ?election_party_7 ?v_4 ?election_party_4  {
            ?v_7 myp:vote ?vote_7 .
            ?vote_7 mypq:valid_votes_recieved ?max_votes_7 ;
                    myps:vote ?election_party_7;
                    .
            ?election_party_7 myd:party/myd:party ?main_party_7 .
            ?v_4 myp:vote ?vote_4 .
            ?vote_4 mypq:valid_votes_recieved ?max_votes_4 ;
                    myps:vote ?election_party_4 ;
                    .
            ?election_party_4 myd:party/myd:party ?main_party_4
            filter(!sameterm(?main_party_4,?main_party_7))
            {
                select ?v_7 (max(?votes) as ?max_votes_7) ?ms ?v_4 ?max_votes_4 {
                    bind(election:pi2021_07 as ?main_election) #use ?main_election for local and parliamentary 
                    ?election myd:main_election ?main_election .
                    #uncomment for local and parliamentary 
                    ?v_7 a my:Voting ;
                         myd:election ?election ;
                         myp:vote/mypq:valid_votes_recieved ?votes ;
                                 myd:section/myd:meta_section ?ms .
                    {
                        select ?v_4 ?ms (max(?votes) as ?max_votes_4) {
                            bind(election:pi2021 as ?main_election) #use ?main_election for local and parliamentary 
                            ?election myd:main_election ?main_election .
                            #uncomment for local and parliamentary 
                            ?v_4 a my:Voting ;
                                 myd:election ?election ;
                                 myp:vote/mypq:valid_votes_recieved ?votes ;
                                         myd:section/myd:meta_section ?ms .
                        } group by ?v_4 ?ms
                    }          
                } group by ?v_7 ?ms ?v_4 ?max_votes_4
            }  
        }
    }

    ?election_party_7 myd:party/myd:party ?main_party_7 .
    ?main_party_7 rdfs:label ?main_party_label_7 .
    ?v_7 a my:Voting ;
         myd:voters_count ?voters_listed_7 ;
         myd:voters_voted_count ?voters_voted_7 ;
         myp:vote ?vote_7, ?vote_7_loser ;
         myd:section ?section_7 ;
         myd:link_html ?protocol_7 ;
         .
    ?vote_7 mypq:valid_votes_recieved ?vote_party_7 ;
            myps:vote ?election_party_7 ;
    .
    ?vote_7_loser mypq:valid_votes_recieved ?vote_party_7_loser ;
               myps:vote/myd:party/myd:party ?main_party_4 ;
    .
    ?section_7 myd:number ?sec_id ;
               myd:place ?place .
    ?place rdfs:label ?place_label  ;
           myd:municipality/rdfs:label ?mun ;
           myd:municipality/myd:province/rdfs:label ?obl ;
    .
    filter(?voters_voted_7 > 50)
    bind(?vote_party_7/?voters_voted_7 as ?vote_ratio_party_7)
    bind(?vote_party_7_loser/?voters_voted_7 as ?vote_ratio_party_7_loser)
    bind(?voters_voted_7/?voters_listed_7 as ?voter_turnover_7) 
    
    ?election_party_4 myd:party/myd:party ?main_party_4 .
    ?main_party_4 rdfs:label ?main_party_label_4 .
    ?v_4 a my:Voting ;
         myd:voters_count ?voters_listed_4 ;
         myd:voters_voted_count ?voters_voted_4 ;
         myp:vote ?vote_4 ;
         myd:vote ?election_party_4 ;
         myd:section ?section_4 ;
         myd:link_html ?protocol_4 ;
         .
    ?vote_4 mypq:valid_votes_recieved ?vote_party_4 ;
            myps:vote ?election_party_4 ;
    .
    filter(?voters_voted_4 > 50)
    bind(?vote_party_4/?voters_voted_4 as ?vote_ratio_party_4)
    bind(?voters_voted_4/?voters_listed_4 as ?voter_turnover_4)    
}
```