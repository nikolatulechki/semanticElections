#WIP query for adding observations

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

select ?locality ?candidate ?election ?local_party ?local_election (sum(?votes) as ?VOTES) where {
    bind(election:pi2021 as ?election)
	{?voting a my:Voting ;
          myd:section/myd:place/myd:municipality?/myd:mir? ?locality}
    union
    {
	 ?voting a my:Voting ;
          myd:election/myd:jurisdiction ?locality ;
          myd:section/myd:place/myd:municipality jurisdiction:2246.
    } union
    {?voting a my:Voting ;
         myd:election/myd:jurisdiction ?locality .
         filter(sameterm(?locality,jurisdiction:32))
    }
    ?voting myd:main_election ?election;
           myd:election ?local_election ;
           myd:voters_voted_count ?voted ;
           myd:voters_count ?voters_list ;
           myp:vote ?vote ;
    .
    ?locality a my:MIR .
    ?election myd:type ?type .
    filter (?type in ("parliamentary"))
    ?vote mypq:valid_votes_recieved ?votes ;
          myps:vote ?local_party .
    ?local_party myd:party+ ?candidate .
    filter not exists {?candidate myd:party []}
} group by ?locality ?candidate ?election ?local_party ?local_election