PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX matched_section: <https://elections.ontotext.com/resource/matched_section/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
clear silent graph graph:sofia_geo_section_match_connect ;
insert {
    graph graph:sofia_geo_section_match_connect {
    ?MSEC_URI a my:МatchedSection ;
        myd:type "geo-match" ;
        myd:number ?num ;
        myd:section ?sec, ?cand .
    ?sec  myd:matched_section ?MSEC_URI .
    ?cand myd:matched_section ?MSEC_URI .
    }
}
where {
    ?sec a my:Section ;
         myd:main_election election:pi2023 ;
         myd:number ?num ;
         myp:geo_match [myps:geo_match ?cand ; mypq:inclusion_ratio ?ratio ] .
    filter(?ratio > 0.50)
    bind(uri(concat(str(matched_section:),?num)) as ?MSEC_URI)
}