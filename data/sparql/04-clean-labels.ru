## Query to clean-up broken labels

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
delete {
    ?s ?p ?label
}
where {
    ?s ?p ?label .
    filter(contains(?label,"��"))
    {
        select ?s ?p (count(*) as ?c) where {
            values ?p {
                rdfs:label
                myd:address
            }
            ?s ?p ?label .
        } group by ?s ?p having(?c>1)
    }
}