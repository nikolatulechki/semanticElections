# DONE single counting of the same result on 2 machines - both for votes and for prefs

fixed using csvtk summing in preprocessing 

https://results.cik.bg/ns2022/protokoli/64/24/244607007.0.html
`sort ../gdrive/data/cikOpenData/pi2022/votes_02.10.2022.flat.txt | uniq -c | sort -rn | grep -v -E ";0$" | less`



# wikidata federation not working 

option 1: figure out how to get rdf out of wikidata directly, probably using curl and a saved query
option 2: fix federation ot post a bug

# my section 
https://results.cik.bg/ns2022/protokoli/64/24/244607007.0.html

# missing ekatte from wd

```sparql
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * {    
{select distinct ?place where { 
    [] myd:place ?place .
    filter not exists {?place myd:municipality []}
} limit 100} 
```

place:99139 https://www.wikidata.org/wiki/Q8438422 
place:97015 https://www.wikidata.org/wiki/Q12293787
place:97029 https://www.wikidata.org/wiki/Q5304836
place:97094 https://www.wikidata.org/wiki/Q12273156
place:98106 https://www.wikidata.org/wiki/Q7780633
place:98065 https://www.wikidata.org/wiki/Q12299038
place:98123 https://www.wikidata.org/wiki/Q7600443
place:98114 https://www.wikidata.org/wiki/Q368259
place:98096 https://www.wikidata.org/wiki/Q12293655
place:97077 https://www.wikidata.org/wiki/Q6590617
place:97080 https://www.wikidata.org/wiki/Q12296885
place:97063 https://www.wikidata.org/wiki/Q12292310
place:97046 https://www.wikidata.org/wiki/Q12297627
place:97149 https://www.wikidata.org/wiki/Q12297627
place:65535 - NA old leftovert ekatte - no sections point to it

# Sections abroad geography 
- there seems to be a stable identifier
- check if it is really stable
- integrate it, reconcile and produce a static mapping with coords from wikidata 
- think of a maintanance workflow  

# Todo 
These places have no geography and seem relevant for local elections 

place:99997 
place:99999
place:99998
place:99996
place:00009
place:99995

# Filipovci has 2 ekatte 

place:97046 vs place:97149 Filipovci

```spqrql
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select * where { 
    values ?place {
        place:97046
        place:97149
    }
	?s myd:place ?place .
} limit 100 
```
https://elections.ontotext.com/resource/section/pi2021_07/254619071
https://elections.ontotext.com/resource/section/pi2021_07/254619070

# mobile sections in 2013

handle this in 2013
П;301800024;ШУМЕН;Каолиново;гр.Каолиново;36079

22	voting:pi2013/%D0%9F/%D0%9F
"24"^^xsd:integer

23	section:pi2013/%D0%9F
"74"^^xsd:integer

# done

(done)
https://elections.ontotext.com/resource/section/pi2021_11/070500114
99944

(done) https://elections.ontotext.com/resource/section/pi2021_11/254618073
place:97032

# (done) missing mun link
https://elections.ontotext.com/resource/section/pi2021_11/020100040

place:56438

49,127,141

### Akf analysis tem queries

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX risky_model: <https://elections.ontotext.com/resource/risky_model/>
select 
(sum(?voted7) as ?sum_voted7)
(sum(?voted11) as ?sum_voted11)
(count(?v11) as ?count)
where { 
	{?v7 a my:Voting ;
    myd:section ?sec7 ;
    myd:main_election election:pi2021_07;
    myd:voters_voted_count ?voted7 ;
    .
    ?sec7 myd:matched_section/myd:risk_model risky_model:akf_all_time_risky ;
    .
    } union {                         
    ?v11 a my:Voting ;
    myd:section ?sec11 ;
    myd:main_election election:pi2021_11;
    myd:voters_voted_count ?voted11 ;
    .
    ?sec11 myd:matched_section/myd:risk_model risky_model:akf_all_time_risky ;
    }
} 


### Party vote ordering

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX seq: <http://www.ontotext.com/plugins/sequences#>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
# Reset sequence so next value will be 1
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
               myd:main_election election:pi2022 ;
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
```