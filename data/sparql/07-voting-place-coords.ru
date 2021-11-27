PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
    ?vp geo:hasGeometry ?ppgeo
}
where {
	?vp a my:VotingPlace ; myd:place/geo:hasGeometry ?ppgeo .
    filter not exists {?vp geo:hasGeometry []}
}