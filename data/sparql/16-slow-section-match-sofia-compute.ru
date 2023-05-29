BASE <https://elections.ontotext.com/resource/>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX ext: <http://rdf.useekm.com/ext#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
clear silent graph graph:sofia_geo_section_match ;
insert {
  graph graph:sofia_geo_section_match {
      ?sec myd:geo_match ?cand ;
           myp:geo_match ?ST_URI .
      ?ST_URI myps:geo_match ?cand ;
           mypq:inclusion_ratio ?int_ratio_norm .
   }
}
#select *
where {
#    bind(<jurisdiction/2246/08> as ?district )
#   bind(<section/pi2023/234602004> as ?sec)
  ?sec  a my:Section ; geo:hasGeometry/geo:asWKT ?sec_geo ; myd:district ?district ; myd:main_election election:pi2023 .

  ?cand a my:Section ; geo:hasGeometry/geo:asWKT ?cand_geo ; myd:district ?district  .
  filter(!sameterm(?sec,?cand))
  filter(geof:sfIntersects(?sec_geo,?cand_geo))
  bind(ext:area(geof:intersection(?sec_geo,?cand_geo)) as ?int_area)
  bind(ext:area(?sec_geo) as ?sec_area)
  bind(?int_area/?sec_area as ?int_ratio)
  filter(?int_ratio > 0.10)
  bind(ceil(?int_ratio*100)/100 as ?int_ratio_norm)
  bind(uri(concat("statement/",str(sha1(concat(str(?sec),str(myd:geo_match),str(?cand)))))) as ?ST_URI)
}