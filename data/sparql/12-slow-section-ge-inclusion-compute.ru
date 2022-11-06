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
clear silent graph graph:sofia_ge_sections ;
insert {
  graph graph:sofia_ge_sections {
      ?sec myd:neighborhood ?ge ;
           myp:neighborhood ?ST_URI .
      ?ST_URI myps:neighborhood ?ge ;
           mypq:inclusion_ratio ?int_ratio_norm .
  }
} where {
#   bind(place:2246\/191 as ?ge)
   ?ge a my:Neighborhood ;
    rdfs:label ?ge_label ;
    geo:hasGeometry/geo:asWKT ?ge_geo ;
   .
  ?sec a my:Section ; geo:hasGeometry/geo:asWKT ?sec_geo .
  filter(geof:sfIntersects(?ge_geo,?sec_geo))
  bind(ext:area(geof:intersection(?ge_geo,?sec_geo)) as ?int_area)
  bind(ext:area(?sec_geo) as ?sec_area)
  bind(?int_area/?sec_area as ?int_ratio)
  filter(?int_ratio > 0.05)
  bind(ceil(?int_ratio*100)/100 as ?int_ratio_norm)
  bind(uri(concat("statement/",str(sha1(concat(str(?sec),str(myd:neighborhood),str(?ge)))))) as ?ST_URI)
}
