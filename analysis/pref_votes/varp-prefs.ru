PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
insert { graph graph:pref_varp {
    ?candidate myd:prefs_varp ?varp .
    }
} where {
select ?candidate ?n (sum(?norm2)/?n as ?varp)   {
{select ?candidate (avg(?cand_preferences) as ?avg) (count(*) as ?n) where {
#    bind(<https://elections.ontotext.com/resource/candidate/pi2021_11/26/17/103> as ?candidate)
    ?pv myps:preference_vote ?candidate ; mypq:valid_votes_recieved ?cand_preferences .
} group by ?candidate }
    ?pv myps:preference_vote ?candidate ; mypq:valid_votes_recieved ?cand_preferences .
    bind(?cand_preferences - ?avg as ?norm)
    bind(?norm*?norm as ?norm2)
    } group by ?candidate ?n }