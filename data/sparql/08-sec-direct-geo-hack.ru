BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
    ?sec geo:hasGeometry ?geo .
}
where {
    ?sec a my:Section ; myd:votingPlace/geo:hasGeometry ?geo .
};

BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

insert {
    ?sec geo:hasGeometry ?geo .
}
where {
    ?sec myd:meta_section/^myd:meta_section ?oth .
    ?oth myd:votingPlace/geo:hasGeometry ?geo .
    ?sec myd:place/^myd:place ?oth .
    filter not exists {?sec geo:hasGeometry [] }
};

BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
    ?sec geo:hasGeometry ?geo .
}
where {
    ?sec myd:place/geo:hasGeometry ?geo .
    filter not exists {?sec geo:hasGeometry [] }
}