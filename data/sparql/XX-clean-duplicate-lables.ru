PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
construct {
    ?s rdfs:label ?L
} where {
    select ?s (sample(?l) as ?L) (count(*) as ?c) where {
        ?s rdfs:label ?l .
    } group by ?s having(?c>1)
}
