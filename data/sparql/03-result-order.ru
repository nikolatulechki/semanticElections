PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX seq: <http://www.ontotext.com/plugins/sequences#>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>

#insert data {
#   my:seq1 seq:drop [] .
#};

insert data {
   my:seq1 seq:create [] .
};
insert data {
   my:seq1 seq:reset [] .
};
insert {
    ?sv mypq:result_order ?order .
}
where {
    {
        select * where {
            ?v a my:Voting ;
               #myd:main_election election:pi2022 ;
               myp:vote ?sv .
            ?sv a my:SectionVote ;
                mypq:valid_votes_recieved ?votes ;
                myps:vote ?party
        } order by ?v desc(?votes) ?party
    }
    my:seq1 seq:nextValue ?order .
};
delete {
    ?sv mypq:result_order ?order .
}
insert {
    ?sv mypq:result_order ?local_order .
}
where {
    { select ?v (min(?order) as ?min) where {
        ?v a my:Voting ; myp:vote ?sv .
        ?sv a my:SectionVote  ; mypq:result_order ?order  .
    } group by ?v }
    ?v myp:vote ?sv .
    ?sv mypq:result_order ?order .
    bind((?order - ?min + 1) as ?local_order)
}