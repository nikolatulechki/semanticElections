#Observations of candidate votes aggregated at the level of GE

BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myc: <https://elections.ontotext.com/resource/prop/cube/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
clear silent graph <graph/cube/ge_votes> ;
insert {
  graph <graph/cube/ge_votes> {
  ?VOTES_URI a qb:Observation , myc:Voting ;
             qb:dataSet <cube/votes> ;
             myc:election ?election ;
             myc:locality ?locality ;
             myc:candidate ?candidate ;
        	 myc:election_candidate ?election_candidate ;
        	 myc:local_candidate  ?local_candidate ;
             myc:local_election ?local_election ;
             myc:activity ?ACT_URI ;
             myc:votes ?VOTES ;
  .

}
}
where {
    {
        select ?locality ?candidate ?election ?local_candidate ?election_candidate ?local_election (sum(?votes) as ?VOTES) where {
#            bind(election:pi2021 as ?election)
 			?voting a my:Voting ;
            myd:section/myp:neighborhood [myps:neighborhood  ?locality ; mypq:isPrimary true] ;
            myd:main_election ?election;
            myd:election ?local_election ;
            myd:voters_voted_count ?voted ;
            myd:voters_count ?voters_list ;
            myp:vote ?vote ;
                    .
            ?election myd:type ?type .
#            filter (?type in ("parliamentary"))
            ?vote mypq:valid_votes_recieved ?votes ;
                  myps:vote ?local_candidate .
            ?local_candidate myd:party+ ?candidate .
            ?local_candidate myd:party+ ?election_candidate .
            ?election_candidate a my:ElectionParty .
            filter not exists {
                ?candidate myd:party []
            }
        } group by ?locality ?candidate ?election ?election_candidate ?local_candidate ?local_election
    }
    bind(uri(concat("cube/votes/",str(sha1(concat(str(?locality),str(?candidate),str(?election)))))) as ?VOTES_URI)
    bind(uri(concat("cube/activity/",str(sha1(concat(str(?locality),str(?election)))))) as ?ACT_URI)
}