PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>
clear silent graph graph:section-districts ;
insert {
    graph graph:section-districts {
    	?sec myd:district ?dis
	}
}
where {
    bind(jurisdiction:2246 as ?mun) #TODO  fix for varna
    ?dis a my:District ; myd:municipality ?mun ; myd:number ?dis_num .
    ?sec a my:Section ; myd:place/myd:municipality ?mun ; myd:number ?sec_num
    bind(substr(?sec_num,5,2) as ?sec_reg)
    filter(?dis_num=?sec_reg)
}