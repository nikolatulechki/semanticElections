PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
clear silent graph graph:geo-match-avg-ratio ;
insert {
    graph graph:geo-match-avg-ratio {
    	?match myd:inclusion_ratio ?RATIO
    }
} where {
{select ?match (avg(?ratio) as ?RATIO) where {
	?match a my:МatchedSection ; myd:type "geo-match" ; myd:section ?sec1, ?sec2 .
    ?sec1 myp:geo_match [myps:geo_match ?sec2 ; mypq:inclusion_ratio ?ratio] .
    filter(!sameterm(?sec1,?sec2))
} group by ?match}
}