# Postprocessing queries 

## Add dates where needed

```sparql
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
    ?el myd:date ?date .
    ?voting myd:date ?date .    
} where { 
    values ?t {
        my:Election 
        my:VotingRound
        my:ElectionRound 
    }
    ?main_el a ?t ; myd:date ?date .
	?el myd:partOf* ?main_el .
    ?voting myd:election ?el .
} 
```

## Query to clean-up broken labels 
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
delete {?s rdfs:label ?label}
#select *
where { 
    ?s rdfs:label ?label .
    filter(contains(?label,"��"))
    {select ?s (count(*) as ?c) where {
        ?s rdfs:label ?label . 
        } group by ?s having(?c>1) }
} 
```
## Party labels from wikidata 

```sparql
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
```

# Analysis queries

## Anomalous sections
Indicator of controlled or bought voting
Sections where a party has received more than 100 votes and has more than and a result in the section more than 2 times higher than its result in the municipality
Example:

Parlamentary 2017, Borovo Municipality GERB have 35.06% of the vote, while in section 190300005 в с.Брестовица, 74.67% of the voters vote for them. 

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select ?sec ?mun_label ?party ?party_label ?total_votes_sec ?sec_party_votes ?sec_party_vote_ratio ?mun_party_votes_total ?mun_party_vote_ratio ?prot_link ?pdf_link {

    ?sec a  my:Section ;
            myd:place/myd:municipality ?mun ;
		    myd:election ?election;		
    .     
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes_sec ;
            myd:vote ?party ;
    		myd:election ?election ;
      		myd:link_html ?prot_link ;
        	myd:link_pdf ?pdf_link ;
    .
    ?vote_st myps:vote ?party ;
#             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?sec_party_votes ;
    .
    ?party rdfs:label ?party_label .
    ?mun rdfs:label ?mun_label .
    bind(floor((?sec_party_votes/?total_votes_sec)*10000)/100 as ?sec_party_vote_ratio)

    filter(?sec_party_votes > 100)
    filter(?sec_party_vote_ratio/?mun_party_vote_ratio > 2)    
    
{select ?election ?mun ?party (sum(?valid_votes) as ?mun_party_votes_total) (floor((sum(?valid_votes)/sum(?total_votes))*10000)/100 as ?mun_party_vote_ratio)
where {
#    bind(<election/mi2019/os> as ?el_filter) # Местни Избори 2019 ОС
    bind(<election/pi2017> as ?el_filter) # Парламент 2017
#   bind(jurisdiction:2246 as ?mun) # Столична община
#	bind(jurisdiction:2105 as ?mun) # община Борино
#    bind(jurisdiction:1539 as ?mun) # община Кнежа 
	
        ?party a my:LocalParty ;
              #myd:candidacy ?election ;
              rdfs:label ?partyName .
        ?voting myp:vote ?vote  ;
                myd:election ?election;
    			myd:votes_valid_count ?total_votes ;
       			myd:section/myd:place/myd:municipality ?mun ;
        .
    	?election myd:partOf* ?el_filter .
        ?vote myps:vote ?party;
            mypq:valid_votes_recieved ?valid_votes ;
        .
     } 
    group by ?election ?mun ?party order by desc(?vote_ratio_mun) }
}
```

## Intra-election comparison of results per section 

Given a section ID, this query outputs the results fore winner of every election compared to mean of winner for all the sections in the location 

```sparql
## Intra-election comparison of results per single section 
# Вот по секции за даден набор партии в дадено населено място 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
select ?sec ?label ?date ?votes_max ?vote_ratio ?el ?party ?party_label (floor((sum(?n_votes_place)/sum(?total_votes_place))*10000)/100 as ?vote_ratio_place){
    ?sec a  my:Section ;
         myd:place ?place ;
    .     
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes ;
            myd:vote ?party ;
    		myd:election ?el ;
            myd:date ?date ;
            rdfs:label ?label ;
    .
    ?vote_st myps:vote ?party ;
             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?votes_max ;
    .
    ?voting_place myd:section/myd:place ?place ;
            myp:vote ?vote_place_st ;
            myd:voters_voted_count ?total_votes_place ;
            myd:vote ?party ;
    .
    ?vote_place_st myps:vote ?party ;
            mypq:valid_votes_recieved ?n_votes_place.
    
    ?party rdfs:label ?party_label ;
    optional{
        ?party myd:party+ ?main_party .
        ?main_party a my:Party ; rdfs:label ?main_label .
    }
    bind(floor((?votes_max/?total_votes)*10000)/100 as ?vote_ratio)
    {select ?sec ?el (max(?n_votes) as ?votes_max){
            
            
            {select ?sec {
                    
#            		bind(<https://elections.ontotext.com/resource/metaSection/153900001> as ?msec) # OK section 
            		bind(<https://elections.ontotext.com/resource/metaSection/153900012> as ?msec) # Anomalous section in Knezha
#                    bind(<https://elections.ontotext.com/resource/metaSection/224607077> as ?msec) # Anomalous section in Sofia - Hr Botev
                    ?sec myd:meta_section ?msec .
                }
                
            }
            ?sec a  my:Section ;
                 myd:place ?place ;
                 .

            ?voting myd:section ?sec ;
                    myp:vote ?vote_st ;
                    myd:voters_voted_count ?total_votes ;
                    myd:vote ?party ;
                    myd:election ?el ;
                    .
            ?vote_st myps:vote ?party ;
                     mypq:type ?vote_type ;
                     mypq:valid_votes_recieved ?n_votes.
            
            ?el rdfs:label ?el_label .
            ?place rdfs:label ?place_label .
        } group by ?sec ?el 
    }
} group by ?sec ?label ?date  ?votes_max ?vote_ratio ?el ?party ?party_label order by desc(?date)
```

Когато братчедите не гласуват с/у когато гласуват (ми2015 / ми2019)
<voting:mi2019/os/2246/224607076> 
<voting:mi2015/os/2246/224607076>

## Sum pref of midlist candidates
Explore extraordinary high preferences for candidates far down the electoral list. Hypotheisi is that such preferences are used as proof of bought votes. 

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select ?cand ?c_lab ?p_lab (sum(?votes) as ?votes_sum) where { 
	?s a my:PreferenceVote ; mypq:valid_votes_recieved ?votes ; myps:preference_vote ?cand .
    ?cand myd:number ?cand_num ; rdfs:label ?c_lab .
    ?cand myd:represents ?party .
    ?party myd:number ?party_num ; rdfs:label ?p_lab .
    filter(?cand_num>10)
    filter(?votes>10)
    filter(?cand_num != ?party_num)
} group by ?cand ?c_lab ?p_lab order by desc(?votes_sum) 
```



## Place level aggregations for 2 parties TODO!

"Swing places" where the voters in one place switch in bulk between two parties 

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>

# wd:Q133968 GERB
# wd:Q164242 DPS


PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select * {
    
bind((?GERB19/?ALLVOTE19 - ?GERB15/?ALLVOTE15) as ?GRTHGERB19)
bind((?DPS19/?ALLVOTE19 - ?DPS15/?ALLVOTE15) as ?GRTHDPS19)
    
{select ?place ?label (sum(?anyvote15) as ?ALLVOTE15) (sum(?gerbvotes15) as ?GERB15) (sum(?dpsvotes15) as ?DPS15) (sum(?anyvote19) as ?ALLVOTE19) (sum(?gerbvotes19) as ?GERB19) (sum(?dpsvotes19) as ?DPS19) 

where { 
    {
        select ?place {
            ?place a my:Place ;
        } limit 100
    } 
    ?place a my:Place ; rdfs:label ?label .
    {
    ?sec15 a my:Section ; myd:place ?place .
 
    ?voting15 myd:section ?sec15 ; myd:election/myd:partOf <election/mi2015/os> .
    ?voting15 myp:vote ?vote15 .
    ?vote15 mypq:valid_votes_recieved ?anyvote15 ; myps:vote ?party15 .

    bind(if(exists{?party15 myd:party+ wd:Q133968},?anyvote15,0) as  ?gerbvotes15)
    bind(if(exists{?party15 myd:party+ wd:Q164242},?anyvote15,0) as  ?dpsvotes15)
    }
    UNION
    {
    ?sec19 a my:Section ; myd:place ?place .
    ?voting19 myd:section ?sec19 ; myd:election/myd:partOf <election/mi2019/os> .
    ?voting19 myp:vote ?vote19 .
    ?vote19 mypq:valid_votes_recieved ?anyvote19 ; myps:vote ?party19 .

    bind(if(exists{?party19 myd:hasPart?/myd:party+ wd:Q133968},?anyvote19,0) as  ?gerbvotes19)
    bind(if(exists{?party19 myd:hasPart?/myd:party+ wd:Q164242},?anyvote19,0) as  ?dpsvotes19)
    }
}
group by ?place ?label}
}

```
## Секции с над 80% избирателна активност.

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
#   bind(<election/mi2019/os> as ?election) # Местни Избори 2019 ОС
#   bind(<election/pi2017> as ?election) # Парламент 2017
    bind(<election/ep2019> as ?election) # ЕП 2019
    ?voting a my:Voting ; 
         myd:election/myd:partOf* ?election  ;
         myd:voters_count ?voters_reg ;
	     myd:voters_additional_count ?voters_add ;
         myd:votes_valid_count ?valid_votes ; 
         myd:link_html ?prot ;
         myd:link_pdf ?pdf ;
         myd:section/rdfs:label ?section_label ;	. 
    bind(?voters_reg+?voters_add as ?voters_tot)
    bind(?valid_votes/?voters_tot as ?voting_activity)
    filter(?voting_activity > 0.8)
}  
#order by desc(?voting_activity) 

```

## Обърнато Гласуване 

- 150-те секции, в които има "обърнато" гласуване между 1 и 2 тур за кмет.
- какво значи по-точно?
- примерно - на първи тур е бил Х с повече гласове, но на втори Y събира повече от него

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX wd: <http://www.wikidata.org/entity/>

select distinct ?election_label ?section_label ?place_label ?cand1_name ?cand2_name ?party1_label ?party2_label ?votes_tur1_c1 ?votes_tur1_c2 ?votes_tur2_c1 ?votes_tur2_c2 ?winner ?t1_ratio ?t2_ratio 

{
    bind(election:mi2019\/ko as ?main_election)
    ?election myd:partOf ?main_election .
    
    ?round1 myd:partOf ?election ; myd:round 1 .
    ?round2 myd:partOf ?election ; myd:round 2 .
    
    ?voting2 a my:Voting ;
               myd:election ?round2 ;
               myd:section ?section ;
               myd:vote ?party1, ?party2 ;
    .
    filter(str(?party1)>str(?party2))
    
    ?election rdfs:label ?election_label .
    ?section rdfs:label ?section_label ; myd:place ?place .
    
    ?place rdfs:label ?place_label .
    
    ?voting2 myp:vote ?v2c1 , ?v2c2 .
    ?v2c1 mypq:valid_votes_recieved ?votes_tur2_c1 ;
          myps:vote ?party1 .
    ?v2c2 mypq:valid_votes_recieved ?votes_tur2_c2 ;
          myps:vote ?party2 .

    ?voting1 a my:Voting ;
             myd:election ?round1 ;
             myd:section ?section ;
             myd:vote ?party1, ?party2 ;
    .

    ?voting1 myp:vote ?v1c1 , ?v1c2 .
    ?v1c1 mypq:valid_votes_recieved ?votes_tur1_c1 ;
          myps:vote ?party1 ;
    .
    ?v1c2 mypq:valid_votes_recieved ?votes_tur1_c2 ;
          myps:vote ?party2 ;
     .
    ## party labels 
    ?party1 rdfs:label ?party1_label .
    ?party2 rdfs:label ?party2_label .
    
   bind(if(?votes_tur2_c1>?votes_tur2_c2,?party1_label,?party2_label) as ?winner)
    
    bind(?votes_tur1_c1/?votes_tur1_c2 as ?t1_ratio)
    bind(?votes_tur2_c1/?votes_tur2_c2 as ?t2_ratio)
    filter ((?t1_ratio < 1 && ?t2_ratio > 1) || (?t1_ratio > 1 && ?t2_ratio < 1) )
    
    ?cand1 myd:represents ?party1 ;
           myd:candidacy ?round2 ; 
           rdfs:label ?cand1_name .     
    ?cand2 myd:represents ?party2 ; 
           myd:candidacy ?round2 ; 
           rdfs:label ?cand2_name . 
}
```

## Top N votes for a given party in a given election

TODO: fix machine voting complications in EP2019

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX wd: <http://www.wikidata.org/entity/>
select ?section_label ?v ?voting_label ?vote_party ?vote_total ?vote_ratio ?protocol
where { 
    
#    bind(wd:Q164242 as ?party) #DPS
    bind(wd:Q133968 as ?party) #GERB
    
    ?election_party myd:party+ ?party .
    
#     bind(election:ep2019 as ?election )

    bind(election:pi2017 as ?main_election) #use ?main_election for local and parliamentary 
    ?election myd:partOf ?main_election . #uncomment for local and parliamentary 
      

    
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:election ?election ;
        myd:votes_valid_count ?vote_total ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section/rdfs:label ?section_label ;
        myd:link_html ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          myps:vote ?election_party ;                      
    .
    filter(?vote_party > 100)
    bind(floor((?vote_party/?vote_total)*10000)/100 as ?vote_ratio)
 
} order by desc(?vote_ratio) limit 500
```

## Candidate Matching analysis

### Names not following the main pattern 

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>        
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * 
where { 
    ?c1 a my:Candidate ; rdfs:label ?l1 .
    filter(!regex(?l1, "^[^ ]+ [^ ]+ [^ ]+$","i"))
} 
```
## Geography 

### nearby voting places

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
select * where { 
    bind(<votingPlace/e4a01f0684b5a1bfbf45a2ae5b846ece5bf9e5f7> as ?p1)
#	?p1 a my:Place .
    ?p2 a my:VotingPlace .  
    ?p1 geo:location/geo:lat ?lat1 ; geo:location/geo:long ?long1 .
    ?p2 geo:location ?geo2 .
    ?geo2 omgeo:nearby(?lat1 ?long1 "10km")
} limit 100 
```

### federation for wikidata places and their GEO

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
prefix wdt: <http://www.wikidata.org/prop/direct/> 

insert {
    graph my:wg-geo-graph {
   	 	?p myd:wdMatch ?q ; geo:location ?POINT .
    	?POINT a geo:Point ; geo:asWKT ?geo .
    }
}
where { 
 	?p a my:Place ; myd:ekatte ?ekatte .
    service <https://query.wikidata.org/sparql> {
        ?q wdt:P3990 ?ekatte ; wdt:P625 ?geo 
    }
    bind(uri(concat(str(?p),"/geo")) as ?POINT)
}
```

### Comparing distance of voting places with center pof place in order to repair google geomatching

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX omgeo: <http://www.ontotext.com/owlim/geo#>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
PREFIX uom: <http://www.opengis.net/def/uom/OGC/1.0/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
#    bind(<place/02676> as ?p1)
    {
        select ?p1 {
            ?vp a my:VotingPlace ; myd:place ?p1. 
        } group by ?p1 having (count(?vp) = 0)
    }
    ?p1 a my:Place ; rdfs:label ?placeLabel .
    ?vp a my:VotingPlace ; myd:place ?p1 ; rdfs:label ?vpLabel .
    ?vp geo:hasGeometry/geo:asWKT ?vpgeo .
    ?p1 geo:hasGeometry/geo:asWKT ?pgeo .
    bind(strdt(str(?vpgeo),<http://www.opengis.net/ont/geosparql#wktLiteral>) as ?newgeo)
    bind(geof:distance(?pgeo, ?newgeo, uom:metre) as ?dist)
    filter(?dist > 15000)
} #limit 100 
```

Postprocessing Q to fix voting places positioned far from their parent places. 
Fallback solution is to place them at the same location as their parent place. 
Will add a flag so that eventually we can look and fix them in the mapping sheets

# Aggregation Queries

TODO in time use these to produce aggregated results for different elections


## Local elections - aggregation on parties
```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX party: <https://elections.ontotext.com/resource/party/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
insert {
    graph <graph/aggregated-results> {
    ?election myd:vote ?party ; myp:vote ?VOTE_URI .
    ?VOTE_URI a my:ElectionVote ;
        myps:vote ?party ;
    	mypq:valid_votes_recieved ?sum_valid_votes ;
        mypq:invalid_votes_recieved ?sum_invalid_votes ;
    .
    }
} 
where {
{select ?election ?party (sum(?valid_votes) as ?sum_valid_votes) (sum(?invalid_votes) as ?sum_invalid_votes) 
    where {
        ?party a my:LocalParty ;
              #myd:candidacy ?election ;
              rdfs:label ?name .
        ?voting myp:vote ?vote  ;
                myd:election ?election .
        ?vote myps:vote ?party;
            mypq:valid_votes_recieved ?valid_votes ;
            mypq:invalid_votes_recieved ?invalid_votes .
     } 
group by ?election ?party }
	bind(uri(concat("vote/",strafter(str(?election),str(election:)),"/",strafter(str(?party),str(party:)))) as ?VOTE_URI)        
}
```

# Integration Queries 

Wikidata Municipalities and Oblast queries. 
Not working need to debug > produces static mapping which is ok for now. 

## Geography 

### Municipalities from Wikidata
```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
	?s a my:Municipality ;
	    rdfs:label ?munLabel ; 
	    myd:mir ?MIRURI ; 
	    myd:province ?obl ; 
	    geo:hasGeometry ?MUN_GEO ; 
	    myd:wdid ?mun .
    ?obl a my:Province ; rdfs:label ?oblLabel .
    ?MUN_GEO a geo:Geometry ; geo:asWKT ?munCoord .        
}
where { 
	?s a my:Municipality ; myd:wdid ?mun .
    service <https://query.wikidata.org/sparql> {
        ?mun wdt:P625 ?munCoord .
        ?mun wdt:P131?/wdt:P7938 ?mir ; wdt:P131 ?obl .
        ?mir p:P31/pq:P1545 ?mirnum ; wdt:P625 ?mirCoord .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg,en". 
            ?mun rdfs:label ?munLabel .
            ?mir rdfs:label ?mirLabel .
            ?obl rdfs:label ?oblLabel .
        }     
    }
    bind(uri(concat(str(jurisdiction:),?mirnum)) as ?MIRURI)
    bind(uri(concat(str(?s),"/geo")) as ?MUN_GEO)
    bind(uri(concat(str(?MIRURI),"/geo")) as ?MIR_GEO)
} 
```
### MIRs from wikidata
```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
	?MIRURI a my:MIR ; rdfs:label ?mirLabel ; geo:hasGeometry ?MIR_GEO ; myd:wdid ?mir ; myd:number ?mirnum .
    ?MIR_GEO a geo:Geometry ; geo:asWKT ?mirCoord .  
}
where { 
    service <https://query.wikidata.org/sparql> {
        ?mir wdt:P31 wd:Q43791141 ; p:P31/pq:P1545 ?mirnum ; wdt:P625 ?mirCoord .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg,en". 
            ?mir rdfs:label ?mirLabel .
        }     
    }
    bind(uri(concat(str(jurisdiction:),?mirnum)) as ?MIRURI)
    bind(uri(concat(str(?s),"/geo")) as ?MUN_GEO)
    bind(uri(concat(str(?MIRURI),"/geo")) as ?MIR_GEO)
}
```

### Places from Wikdata

```sparql
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX place: <https://elections.ontotext.com/resource/place/> 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
construct {
    ?PLACE_URI a my:Place ;
               rdfs:label ?placeLabel ;
               myd:municipality ?s ;
               geo:hasGeometry ?PLACE_GEO_URI ;
               myd:idwd ?place ;
    .
    ?PLACE_GEO_URI a geo:Geometry ; geo:asWKT ?placeCoord . 
} where { 
	?s myd:wdid ?mun
    service <https://query.wikidata.org/sparql> {
        ?place wdt:P131 ?mun ; p:P3990 ?ekst ; wdt:P625 ?placeCoord .
        ?ekst ps:P3990 ?ekatte .
        filter not exists {?ekst pq:P518 [] }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "bg". 
            ?place rdfs:label ?placeLabel .
        }
    bind(uri(concat(str(place:),?ekatte)) as ?PLACE_URI)
    bind(uri(concat(str(place:),?ekatte,"/geo")) as ?PLACE_GEO_URI)   
    }
}
```
## Create metasections based on sections with matching ID

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
insert {
graph <graph/metasections> {	
	?metasec a my:MetaSection .
    ?sec  myd:meta_section ?metasec .    
}}
where {
    ?sec a my:Section ; myd:number ?num .
    bind(uri(concat("metaSection/",?num)) as ?metasec)
}
```

## Generate MI2015 local party mappings
for export to google sheet

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?loc (group_concat(distinct ?num;separator=";") as ?nums) where { 
	?loc a my:LocalParty ; rdfs:label ?locLabel  ; myd:candidacy/myd:partOf+ election:mi2015 .
    ?main a my:ElectionParty ; rdfs:label ?mainLabel ; myd:candidacy election:mi2015 ; myd:number ?num .
    filter(contains(lcase(?locLabel),lcase(?mainLabel)))
    filter(!sameterm(?main,<party/mi2015/75>)) #шибаните зелени
} group by ?loc
```