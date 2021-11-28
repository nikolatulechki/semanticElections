BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
    ?sec geo:hasGeometry ?geo .
}
where {
    ?sec a my:Section ; myd:votingPlace ?vp .
    ?vp geo:hasGeometry ?geo ; myd:place/^myd:place ?sec .
};

BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX election: <https://elections.ontotext.com/resource/election/>

insert {
    ?sec geo:hasGeometry ?geo .
}
#select ?sec (count(distinct ?vp) as ?c)
where {
    ?sec myd:meta_section/^myd:meta_section ?oth .
    ?oth myd:votingPlace ?vp ; myd:main_election election:pi2017 .
    ?vp geo:hasGeometry ?geo ; myd:place/^myd:place ?sec .
    ?sec myd:place/^myd:place ?oth .

    filter not exists {?sec geo:hasGeometry [] }
} ;
#group by ?sec order by desc(?c)

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