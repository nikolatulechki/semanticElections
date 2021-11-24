# Add Direct main election links .

PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
    ?el myd:main_election ?main_el .
    ?voting myd:main_election ?main_el .
} where {
    ?main_el a my:Election ; myd:type [] .
	?el myd:partOf* ?main_el .
    ?voting myd:election ?el .
}