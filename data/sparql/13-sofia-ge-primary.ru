PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
clear silent graph graph:sofia_ge_primary ;
insert {
    graph graph:sofia_ge_primary {
        ?statement mypq:isPrimary true ;
    }
}
where {
    {
        select ?sec (max(?ratio) as ?MAX) where {
            ?sec myp:neighborhood ?statement .
            ?statement mypq:inclusion_ratio ?ratio .
        } group by ?sec
    }
    ?statement ^myp:neighborhood ?sec ;
                mypq:inclusion_ratio  ?MAX .
} ;