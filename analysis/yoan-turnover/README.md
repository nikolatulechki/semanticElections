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