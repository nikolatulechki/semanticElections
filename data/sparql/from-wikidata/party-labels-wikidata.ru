## Party labels from wikidata

PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
insert {
    ?wd rdfs:label ?wdLabel .
} where {
	?wd a my:Party
    service <https://query.wikidata.org/sparql> {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg,en".
            ?wd rdfs:label ?wdLabel .
        }
    }
}