BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
	?metasec a my:MetaSection .
    ?sec  myd:meta_section ?metasec .
}
where {
    ?sec a my:Section ; myd:number ?num .
    bind(uri(concat("metaSection/",?num)) as ?metasec)
}