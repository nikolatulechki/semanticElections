insert {
    graph <{{graph}}> {
        ?org trr:name ?preferred
    }
} where {
	{
	    select ?org (min(?altName) as ?preferred)
        where {
	        ?org a trr:Organization;
		    trr:altName ?altName;
        } group by ?org
    }
}
