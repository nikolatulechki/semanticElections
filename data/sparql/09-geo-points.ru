PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
 ?point geo:lat ?lat ;
        geo:long ?lon .

} where {
	?point a geo:Geometry ; geo:asWKT ?wkt .
    bind(xsd:float(replace(strafter(str(?wkt),"Point(")," .*","")) as ?lon)
    bind(xsd:float(replace(strafter(str(?wkt),"Point("),"([0-9]|\\.)* |\\)","")) as ?lat)
}`