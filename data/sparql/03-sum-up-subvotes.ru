## Sum up sub_votes  pi2021_07 and pi2021_11

PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
insert {
    ?vote mypq:valid_votes_recieved ?VOTES .
} where
{ select ?vote (sum(?votes) as ?VOTES) where {
    ?vote mypq:sub_votes ?votes .
} group by ?vote }
