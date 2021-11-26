PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?party ?label ?n (sum(?norm2)/?n as ?varp)   {
    {
        select ?party (avg(?cand_preferences) as ?avg) (count(*) as ?n) where {
            #    bind(<https://elections.ontotext.com/resource/candidate/pi2021_11/26/17/103> as ?candidate)
            ?pv myps:preference_vote ?cand ;
                mypq:valid_votes_recieved ?cand_preferences .
            ?cand myd:represents/myd:party ?party ; myd:number ?num .
            ?party myd:candidacy election:pi2021_11 .
        } group by ?party
    }
    ?party rdfs:label ?label .
    ?pv myps:preference_vote/myd:represents/myd:party ?party ;
        mypq:valid_votes_recieved ?cand_preferences .
    bind(?cand_preferences - ?avg as ?norm)
    bind(?norm*?norm as ?norm2)
} group by ?party ?label ?n