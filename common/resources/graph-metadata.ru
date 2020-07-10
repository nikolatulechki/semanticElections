insert {
    graph ?graph {
            ?graph
                trr:updatedOn ?now ;
                trr:version "${{dag_version}}", "${{pipeline_version}}" ;
                trr:triplesCount "${{triples}}" ;
        }
} where {
    bind(<{{graph}}> as ?graph)
    bind(now() as ?now)
}