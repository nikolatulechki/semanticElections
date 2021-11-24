# Add dates where needed

PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
    ?el myd:date ?date .
    ?voting myd:date ?date .
} where {
    values ?t {
        my:Election
        my:VotingRound
        my:ElectionRound
    }
    ?main_el a ?t ; myd:date ?date .
	?el myd:partOf* ?main_el .
    ?voting myd:election ?el .
}