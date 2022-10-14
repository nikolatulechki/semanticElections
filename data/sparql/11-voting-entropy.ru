PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX ofn: <http://www.ontotext.com/sparql/functions/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>

insert {
    graph graph:entropy {
        ?voting myd:entropy ?entropy .
    }
} where {
    {
        select ?voting (-sum(?en_vote) as ?entropy)
        where {
            ?sec a my:Section ;
                 rdfs:label ?lab .
            ?voting myd:section ?sec ;
                    myd:voters_voted_count ?voters ;
                    myp:vote ?vote .
            ?vote mypq:valid_votes_recieved ?votes .
            filter(?voters>10)
            bind(?votes/?voters as ?pvote)
            bind(ofn:log(?pvote) as ?log_pvote)
            bind(?pvote*?log_pvote as ?en_vote)
            filter(?log_pvote != "-INF"^^xsd:double)
#            filter(contains(str(?voting),"mi2019"))
        }
        group by ?voting
    }
}