# List of SPARQL Queries

<!--TOC-->

- [Postprocessing queries ](#postprocessing-queries-)
    - [Add dates where needed](#add-dates-where-needed)
    - [Query to clean-up broken labels ](#query-to-clean-up-broken-labels-)
    - [Party labels from wikidata ](#party-labels-from-wikidata-)
- [Analysis queries](#analysis-queries)
    - [Anomalous sections](#anomalous-sections)
    - [Elections Abroad](#elections-abroad)
    - [Intra-election comparison of results per section ](#intra-election-comparison-of-results-per-section-)
    - [Gurkovo](#gurkovo)
    - [Hristo Botev local anomaly (ми2015 / ми2019)](#hristo-botev-local-anomaly-ми2015--ми2019)
    - [Sum pref of midlist candidates](#sum-pref-of-midlist-candidates)
    - [Place level aggregations for 2 parties TODO!](#place-level-aggregations-for-2-parties-todo)
    - [Секции с над 80% избирателна активност.](#секции-с-над-80-избирателна-активност)
    - [Обърнато Гласуване ](#обърнато-гласуване-)
    - [Top N votes for a given party in a given election](#top-n-votes-for-a-given-party-in-a-given-election)
    - [Vote winners vs turnover](#vote-winners-vs-turnover)
        - [Local ](#local-)
        - [EP](#ep)
        - [Presidential ](#presidential-)
        - [Parliamentary](#parliamentary)
    - [Candidate Matching analysis](#candidate-matching-analysis)
        - [Names not following the main pattern ](#names-not-following-the-main-pattern-)
    - [Geography ](#geography-)
    - [MAP Sections on YASGUI](#map-sections-on-yasgui)
        - [Sections with more than 80% turnover](#sections-with-more-than-80-turnover)
        - [nearby voting places](#nearby-voting-places)
        - [federation for wikidata places and their GEO](#federation-for-wikidata-places-and-their-geo)
        - [Comparing distance of voting places with center pof place in order to repair google geomatching](#comparing-distance-of-voting-places-with-center-pof-place-in-order-to-repair-google-geomatching)
- [Aggregation Queries](#aggregation-queries)
    - [Local elections - aggregation on parties](#local-elections---aggregation-on-parties)
- [Integration Queries ](#integration-queries-)
    - [Geography ](#geography--1)
        - [Municipalities from Wikidata](#municipalities-from-wikidata)
        - [MIRs from wikidata](#mirs-from-wikidata)
        - [Places from Wikdata](#places-from-wikdata)
    - [Create metasections based on sections with matching ID](#create-metasections-based-on-sections-with-matching-id)
    - [Generate MI2015 local party mappings](#generate-mi2015-local-party-mappings)
- [Dump and export](#dump-and-export)

<!--TOC-->

## Add enrtropy to votings

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX ofn: <http://www.ontotext.com/sparql/functions/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX graph: <https://elections.ontotext.com/resource/graph/>

insert {
    graph graph:entropy {
         .
    }
} where {
    {
        select ?voting (-sum(?en_vote) as ?entropy)
        where {
            ?sec a my:Section ;
                 rdfs:label ?lab .
            ?voting myd:section ?sec ;
                    myd:voters_voted_count ?voters ;
                    myd:date ?date ;
                    myd:election/rdfs:label ?election_label ;
                                myd:link_html ?protocol ;
                                .
            ?voting myp:vote ?vote .
            ?vote mypq:valid_votes_recieved ?votes .
            filter(?voters>10)
            bind(?votes/?voters as ?pvote)
            bind(ofn:log(?pvote) as ?log_pvote)
            bind(?pvote*?log_pvote as ?en_vote)
            filter(?log_pvote != "-INF"^^xsd:double)
#            filter(contains(str(?voting),"mi2019")) 
        } 
        group by ?voting 
    }
} 
```

## Place population from wikidata

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX place: <https://elections.ontotext.com/resource/place/>

insert {
    graph <graph/place-population> {
    	?place myd:population ?pop .
	}
}
where { 
    bind(uri(concat(str(place:),?ekatte)) as ?place)
    ?place a my:Place .
    service <https://query.wikidata.org/sparql> {
        select ?ekatte ?pop {
        	?wd p:P1082 ?pops ; wdt:P3990 ?ekatte .
        	?pops pq:P459 wd:Q90878157 ; ps:P1082 ?pop .
        }
    }
}
```

## Postmortem for missing pi2013 places

TODO fix this at source, probably pb with missing leading zeroes

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
insert {
    ?s13 myd:place ?place .
}
where { 
	?s17 a my:Section ; myd:main_election election:pi2017 ; myd:place ?place .
	?s13 a my:Section ; myd:main_election election:pi2013 .
    ?s13 myd:number/^myd:number ?s17 .
    filter not exists {?s13 myd:place [] }
} 
```

# Analysis queries

## Stats Query for the demonstartor page

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select * {
    {select (count(*) as ?n_el) {
            ?x a my:Election ;
               myd:type []
    }}
    {select (count(*) as ?party) {
            ?x a my:Party .
    }}
    {select (sum(?pref) as ?pref_votes) {
            ?x a my:PreferenceVote ; mypq:valid_votes_recieved ?pref.
    }}
    {select (sum(?vote) as ?votes) {
            ?x a my:SectionVote ; mypq:valid_votes_recieved ?vote.
    }}
    {select (count(*) as ?sections) {
            ?x a my:Section.
    }}
    {select (count(*) as ?candidates) {
            ?x a my:Candidate.
    }}
    {select (count(*) as ?protocols) {
            ?x a my:Voting.
    }}
    {select (count(*) as ?triples) {
            ?s ?p ?o .
    }}
}
```

## Preference analysis of a single candidate - 

GSheet [pivot](https://docs.google.com/spreadsheets/d/10VJCxktNmaPdUUHphrnluQNR_86DQQnCJdb_U8YDHsw/edit#gid=1736458899) 

```sparql
# pref votes for a single candidate

BASE  <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
select ?date ?party_label ?cand_number ?cand_name ?obl ?mun ?place ?sec_id ?cand_preferences ?party_votes ?pref_ratio ?protocol where { 
    
   {select * where { 
            ?candidate a my:Candidate ; rdfs:label ?lab ; myd:candidacy ?el .
            optional{?el rdfs:label ?elLabel }
            filter(contains(lcase(?lab),"красен георгиев кръстев"))
    }}
    
    ?candidate a my:Candidate ; myd:represents ?localParty  ; myd:candidacy ?el ; rdfs:label ?cand_name ; myd:number ?cand_number . 
    ?voting myp:preference_vote ?pv ; myp:vote ?v ;  myd:section ?section ; myd:link_html ?protocol ; myd:date ?date .
    ?v myps:vote ?localParty ; mypq:valid_votes_recieved ?party_votes .
    ?pv myps:preference_vote ?candidate ; mypq:valid_votes_recieved ?cand_preferences .
    ?localParty rdfs:label ?party_label .
    ?section myd:number ?sec_id ; 
             myd:place/rdfs:label ?place ;
             myd:place/myd:municipality/rdfs:label ?mun ;
             myd:place/myd:municipality/myd:province/rdfs:label ?obl ;
    .
    
    bind(floor((?cand_preferences/?party_votes)*10000)/100 as ?pref_ratio)
    
} order by desc(?cand_preferences)
```



## Entropy in votes

Minimum entropy is when everybody in a section voted for 1 party

```sparql 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX ofn: <http://www.ontotext.com/sparql/functions/>

PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
select 
?voting ?sec ?lab ?election_label  ?protocol (-sum(?en_vote) as ?entropy)
where {
    ?sec a my:Section ;
         rdfs:label ?lab .
    ?voting myd:section ?sec ;
            myd:voters_voted_count ?voters ;
            myd:date ?date ;
            myd:election/rdfs:label ?election_label ;
    		myd:link_html ?protocol ;
     .
    ?voting myp:vote ?vote .
    ?vote mypq:valid_votes_recieved ?votes .
    filter(?voters>200)
    bind(?votes/?voters as ?pvote)
    bind(ofn:log(?pvote) as ?log_pvote)
    bind(?pvote*?log_pvote as ?en_vote)
    filter(?log_pvote != "-INF"^^xsd:double)
    filter(contains(str(?voting),"mi2019")) 
} 
group by ?voting ?sec ?lab ?election_label ?protocol 
order by ?entropy 
```

## Anomalous sections

Indicator of controlled or bought voting Sections where a party has received more than 100 votes and has more than and a
result in the section more than 2 times higher than its result in the municipality Example:

Parlamentary 2017, Borovo Municipality GERB have 35.06% of the vote, while in section 190300005 в с.Брестовица, 74.67%
of the voters vote for them.

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

## Elections Abroad

Kludge for pi2017 - reason fucked up parites

```spaqrl
## Winners abroad  
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX party: <https://elections.ontotext.com/resource/party/>
select ?sec ?sec_label ?date ?total_votes ?votes_winner ?vote_ratio ?el ?el_label ?party ?party_label {
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
             mypq:valid_votes_recieved ?votes_winner ;
    .
    bind(uri(concat(str(party:),"pi2017",strafter(str(?party),"https://elections.ontotext.com/resource/party/pi2017/32"))) as ?party_ok)
    ?party_ok rdfs:label ?party_label .
	?sec rdfs:label ?sec_label .
    ?el rdfs:label ?el_label .
    bind(floor((?votes_winner/?total_votes)*10000)/100 as ?vote_ratio)
    {select ?sec ?el (max(?n_votes) as ?votes_winner){
            #subquery 2 - selects tne maximum votes in each voting .
            {select ?sec {
                #subquery 1 - sections abroad start with 32   
                ?sec a my:Section ; myd:number ?num
                filter(strstarts(str(?num),"32"))
                }
            }
            ?voting myd:section ?sec ;
                    myp:vote ?vote_st ;
                    myd:voters_voted_count ?total_votes ;
                    myd:vote ?party ;
                    myd:election election:pi2017\/32 ;
                    .
            ?vote_st myps:vote ?party ;
                     mypq:type ?vote_type ;
                     mypq:valid_votes_recieved ?n_votes.
            
        } group by ?sec ?el 
    }
    
} group by ?sec ?sec_label ?date ?total_votes ?votes_winner ?vote_ratio ?el ?el_label ?party ?party_label order by desc(?date) str(?sec)
```

```sparql
## Winners abroad  
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select ?sec ?sec_label ?date ?total_votes ?votes_winner ?vote_ratio ?el ?el_label ?party ?party_label {
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
             mypq:valid_votes_recieved ?votes_winner ;
    .
    ?party rdfs:label ?party_label .
	?sec rdfs:label ?sec_label .
    ?el rdfs:label ?el_label .
    bind(floor((?votes_winner/?total_votes)*10000)/100 as ?vote_ratio)
    {select ?sec ?el (max(?n_votes) as ?votes_winner){
            #subquery 2 - selects tne maximum votes in each voting .
            {select ?sec {
                #subquery 1 - sections abroad start with 32   
                ?sec a my:Section ; myd:number ?num
                filter(strstarts(str(?num),"32"))
                }
            }
            ?voting myd:section ?sec ;
                    myp:vote ?vote_st ;
                    myd:voters_voted_count ?total_votes ;
                    myd:vote ?party ;
                    myd:election ?el ;
                    .
            ?vote_st myps:vote ?party ;
                     mypq:type ?vote_type ;
                     mypq:valid_votes_recieved ?n_votes.
            
        } group by ?sec ?el 
    }
} group by ?sec ?sec_label ?date ?total_votes ?votes_winner ?vote_ratio ?el ?el_label ?party ?party_label order by desc(?date) str(?sec)
```

## Intra-election comparison of results for a given party

```sparql
## GERB votes local elections 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?sec_num ?voters_15 ?voted_15 ?party_votes_15 ?voters_19 ?voted_19 ?party_votes_19 ?prot_15 ?prot_19  {
    ?sec_15 myd:meta_section/^myd:meta_section ?sec_19 ; myd:number ?sec_num . 
    ?voting_15 myd:section ?sec_15 ;
            myp:vote ?vote_st_15 ;
            myd:voters_count ?voters_15 ;
            myd:voters_voted_count ?voted_15 ;
            myd:vote ?party_15 ;
            myd:link_html ?prot_15 ;
    		myd:main_election election:mi2015 ;
    .
    filter(contains(str(?voting_15),"ko/tur2")) 
    ?vote_st_15 myps:vote ?party_15 ;
             mypq:valid_votes_recieved ?party_votes_15 ;
    .
    ?party_15 myd:party/myd:party wd:Q133968 .
        ?voting_19 myd:section ?sec_19 ;
            myp:vote ?vote_st_19 ;
            myd:voters_count ?voters_19 ;
            myd:voters_voted_count ?voted_19 ;
            myd:vote ?party_19 ;
            myd:link_html ?prot_19 ;
    		myd:main_election election:mi2019 ;
    .
    filter(contains(str(?voting_19),"ko/tur2")) 
    ?vote_st_19 myps:vote ?party_19 ;
             mypq:valid_votes_recieved ?party_votes_19 ;
    .
    ?party_19 myd:party/myd:party wd:Q133968 .
} 
```

## Intra-election comparison of results per section

Given a section ID, this query outputs the results fore winner of every election compared to mean of winner for all the
sections in the location

```sparql
## Intra-election comparison of results per single section 
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

## Gurkovo

```sparql
## Intra-election comparison of results per single section 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select ?sec ?sec_num ?label ?date ?voters_list ?total_votes  ?votes_max ?vote_ratio ?el ?party ?party_label (floor((sum(?n_votes_place)/sum(?total_votes_place))*10000)/100 as ?vote_ratio_place) ?prot_link ?pdf_link {
    ?sec a  my:Section ;
         myd:place/myd:municipality ?place ;
         myd:number ?sec_num ;
    .     
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_count ?voters_list ;
            myd:voters_voted_count ?total_votes ;
            myd:link_html ?prot_link ;
            myd:link_pdf ?pdf_link ;
            myd:vote ?party ;
    		myd:election ?el ;
            myd:date ?date ;
            rdfs:label ?label ;
    .
    ?vote_st myps:vote ?party ;
             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?votes_max ;
    .
    ?voting_place myd:section/myd:place/myd:municipality ?place ;
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
            
            
            {select distinct ?sec {
                    ?sec myd:meta_section/^myd:meta_section/myd:place/myd:municipality jurisdiction:2437 
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
} group by ?sec ?sec_num ?label ?date ?total_votes  ?votes_max ?vote_ratio ?el ?party ?party_label ?prot_link ?pdf_link ?voters_list order by desc(?sec_num) desc(?date)

```

## Hristo Botev local anomaly (ми2015 / ми2019)

```spaqrl
## Intra-election comparison of results per single section 
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
select ?sec ?sec_num ?label ?date ?voters_list ?total_votes  ?votes_max ?vote_ratio ?el ?party ?party_label (floor((sum(?n_votes_place)/sum(?total_votes_place))*10000)/100 as ?vote_ratio_place) ?prot_link ?pdf_link {
    ?sec a  my:Section ;
         myd:place ?place ;
         myd:number ?sec_num ;
    .     
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_count ?voters_list ;
            myd:voters_voted_count ?total_votes ;
            myd:link_html ?prot_link ;
            myd:link_pdf ?pdf_link ;
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
            
            
            {select distinct ?sec {
                    ?sec myd:meta_section/^myd:meta_section/myd:votingPlace <https://elections.ontotext.com/resource/votingPlace/bc453f1580fef97f05e8f2db96a2bc9bec813595>
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
} group by ?sec ?sec_num ?label ?date ?total_votes  ?votes_max ?vote_ratio ?el ?party ?party_label ?prot_link ?pdf_link ?voters_list order by desc(?sec_num) desc(?date)
```

<voting:mi2019/os/2246/224607076>
<voting:mi2015/os/2246/224607076>

## Sum pref of midlist candidates

Explore extraordinary high preferences for candidates far down the electoral list. Hypotheisi is that such preferences
are used as proof of bought votes.

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
select ?sec_id ?pref_total ?pref_votes ?party_num ?cand_num ?party_name ?cand_name where { 
    {select ?v (sum(?pref) as ?pref_total) {
    ?v myd:main_election election:pi2021 ; 
       myp:preference_vote/mypq:valid_votes_recieved ?pref .   
    } group by ?v }
	?v myp:preference_vote ?s ; myd:section/myd:number ?sec_id .
    ?s a my:PreferenceVote ; mypq:valid_votes_recieved ?pref_votes ; myps:preference_vote ?cand .
    ?cand myd:number ?cand_num ; rdfs:label ?cand_name .
    ?cand myd:represents ?party .
    ?party myd:number ?party_num ; rdfs:label ?party_name .
    filter(?cand_num>103)
    filter(?pref_votes>15)
} order by ?sec_id desc(?pref_votes)
```

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

## Vote winners vs turnover

Inspired by "Statistical fingerprints of electoral
fraud" [pdf](https://rss.onlinelibrary.wiley.com/doi/epdf/10.1111/j.1740-9713.2016.00936.x)

### Local

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
select ?v ?voting_label ?vote_party ?voters_voted ?section_label ?election_party_label ?vote_ratio_party ?voter_turnover ?protocol 
where { 
              
    ?election_party rdfs:label ?election_party_label
    
    {select ?v ?election_party {
        ?v myp:vote ?vote .
        ?vote mypq:valid_votes_recieved ?max_votes ; 
          myps:vote ?election_party ;  
         .
        {select ?v (max(?votes) as ?max_votes) {
#           bind(election:ep2019 as ?election )
            bind(election:mi2019\/ko as ?main_election) #use ?main_election for local and parliamentary 
            ?election myd:partOf/myd:partOf ?main_election . #uncomment for local and parliamentary 
            ?v a my:Voting ; myd:election ?election ; myp:vote/mypq:valid_votes_recieved ?votes            
        } group by ?v }  
    }}
    
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:election ?election ;
        myd:voters_count ?voters_listed ;
        myd:voters_voted_count ?voters_voted ;
        myd:voters_additional_count ?voters_additional ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section/rdfs:label ?section_label ;
        myd:link_html ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          myps:vote ?election_party ;                      
    .
#    filter(?vote_party > 100)
    bind(floor((?vote_party/?voters_voted)*10000)/100 as ?vote_ratio_party)
    bind(floor((?voters_voted/(?voters_listed+?voters_additional))*10000)/100 as ?voter_turnover)
    
} 
``` 

### EP

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
select ?v ?voting_label ?vote_party ?voters_voted ?section_label ?election_party_label ?vote_ratio_party ?voter_turnover ?protocol 
where { 
              
    ?election_party rdfs:label ?election_party_label
    
    {select ?v ?election_party {
        ?v myp:vote ?vote .
        ?vote mypq:valid_votes_recieved ?max_votes ;
          myps:vote ?election_party ;  
         .
        {select ?v (max(?votes) as ?max_votes) {
           bind(election:ep2019 as ?election )
#            bind(election:mi2019\/ko as ?main_election) #use ?main_election for local and parliamentary 
#            ?election myd:partOf/myd:partOf ?main_election . #uncomment for local and parliamentary 
            ?v a my:Voting ; myd:election ?election ; myp:vote/mypq:valid_votes_recieved ?votes            
        } group by ?v }  
    }}
    
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:election ?election ;
        myd:voters_count ?voters_listed ;
        myd:voters_voted_count ?voters_voted ;
        myd:voters_additional_count ?voters_additional ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section/rdfs:label ?section_label ;
        myd:link_html ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          mypq:type "paper" ;
          myps:vote ?election_party ;                      
    .
#    filter(?vote_party > 100)
    bind(floor((?vote_party/?voters_voted)*10000)/100 as ?vote_ratio_party)
    bind(floor((?voters_voted/(?voters_listed+?voters_additional))*10000)/100 as ?voter_turnover)
    
} 
```

### Presidential

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
select ?v ?voting_label ?vote_party ?voters_voted ?section_label ?election_party_label ?vote_ratio_party ?voter_turnover ?protocol 
where { 
              
  
    bind(election:pvnr2016 as ?main_election) #use ?main_election for local and parliamentary 
    ?election myd:partOf ?main_election . #uncomment for local and parliamentary

#   bind(party:pvnr2016\/13 as ?election_party) #RADEV
    bind(party:pvnr2016\/17 as ?election_party) #GERB
    
    filter(?vote_ratio_party > 60)
    filter(?voter_turnover > 80)
    
    ?election_party rdfs:label ?election_party_label .
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:round 2 ; #voting round for presidential ;       
        myd:election ?election ;
        myd:voters_count ?voters_listed ;
        myd:voters_voted_count ?voters_voted ;
        myd:voters_additional_count ?voters_additional ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section/rdfs:label ?section_label ;
        myd:link_html ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          mypq:type "paper" ;
          myps:vote ?election_party ;                      
    .
#    filter(?vote_party > 100)
    bind(floor((?vote_party/?voters_voted)*10000)/100 as ?vote_ratio_party)
    bind(floor((?voters_voted/(?voters_listed+?voters_additional))*10000)/100 as ?voter_turnover)    
}
```

### Parliamentary

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
select ?v ?voting_label ?vote_party ?voters_voted ?section_label ?election_party_label ?vote_ratio_party ?voter_turnover ?protocol 
where { 
              
    ?election_party rdfs:label ?election_party_label
    
    {select ?v ?election_party {
        ?v myp:vote ?vote .
        ?vote mypq:valid_votes_recieved ?max_votes ;
          myps:vote ?election_party ;  
         .
        {select ?v (max(?votes) as ?max_votes) {
#           bind(election:ep2019 as ?election )
            bind(election:pi2017 as ?main_election) #use ?main_election for local and parliamentary 
            ?election myd:partOf ?main_election . #uncomment for local and parliamentary 
            ?v a my:Voting ; myd:election ?election ; myp:vote/mypq:valid_votes_recieved ?votes            
        } group by ?v }  
    }}
    
    ?v a my:Voting ; 
        rdfs:label ?voting_label ;
        myd:election ?election ;
        myd:voters_count ?voters_listed ;
        myd:voters_voted_count ?voters_voted ;
        myd:voters_additional_count ?voters_additional ;
        myp:vote ?vote ;
        myd:vote ?election_party ;
        myd:section/rdfs:label ?section_label ;
        myd:link_html ?protocol ;         
    .
    ?vote mypq:valid_votes_recieved ?vote_party ; 
          mypq:type "paper" ;
          myps:vote ?election_party ;                      
    .
#    filter(?vote_party > 100)
    bind(floor((?vote_party/?voters_voted)*10000)/100 as ?vote_ratio_party)
    bind(floor((?voters_voted/(?voters_listed+?voters_additional))*10000)/100 as ?voter_turnover)    
} 
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

## MAP Sections on YASGUI

### Sections with more than 80% turnover

<https://api.triplydb.com/s/5xCFWepKC>

Query on for yasgui

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select * where { 
   bind(<election/mi2019/ko/tur2> as ?election) # Местни Избори 2019 ОС
#   bind(<election/pi2017> as ?election) # Парламент 2017
#    bind(<election/ep2019> as ?election) # ЕП 2019
    ?voting a my:Voting ; 
         myd:election/myd:partOf ?election  ;
         myd:voters_count ?voters_reg ;
	     myd:voters_additional_count ?voters_add ;
         myd:votes_valid_count ?valid_votes ; 
         myd:link_html ?prot ;
         myd:link_pdf ?pdf ;
         myd:section ?section 
     .  
    ?section rdfs:label ?section_label ;	
             myd:votingPlace ?place   				
             . 
    ?place geo:hasGeometry/geo:asWKT ?x ; rdfs:label ?xTooltip 
    bind(?voters_reg+?voters_add as ?voters_tot)
    bind(?valid_votes/?voters_tot as ?voting_activity)
#    bind(?voting_activity as ?xTooltip)
#  	bind(?prot as ?xLabel)
  	bind(floor(?voting_activity*10000)/100 as ?voter_activity_ratio)
  bind(strdt(concat("<p>",?section_label," ",str(?voter_activity_ratio),"% <a href=\"",str(?prot),"\">prot</a></p>"),rdf:HTML) as ?xLabel)  
  filter(?voting_activity > 0.8) 
} 
```  

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

Postprocessing Q to fix voting places positioned far from their parent places. Fallback solution is to place them at the
same location as their parent place. Will add a flag so that eventually we can look and fix them in the mapping sheets

## Comparing population with sum of registered voters

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX place: <https://elections.ontotext.com/resource/place/>
select 
?mun_label ?place_label ?ekatte ?pop 
(sum(?pi2013) as ?PI2013) 
(sum(?pi2014) as ?PI2014) 
(sum(?pi2017) as ?PI2017) 
(sum(?mi2015) as ?MI2015) 
(sum(?mi2019) as ?MI2019) 
(sum(?ep2019) as ?EP2019) 
(sum(?pvnr2016) as ?PVNR2016) 
where { 
	?voting a my:Voting ; myd:section ?sec ; myd:voters_count ?voters .
    bind(if(contains(str(?voting),"pi2013"),?voters,0) as ?pi2013)
    bind(if(contains(str(?voting),"pi2014"),?voters,0) as ?pi2014)
    bind(if(contains(str(?voting),"mi2015/os"),?voters,0) as ?mi2015)
    bind(if(contains(str(?voting),"pvnr2016/tur1"),?voters,0) as ?pvnr2016)
    bind(if(contains(str(?voting),"pi2017"),?voters,0) as ?pi2017)
    bind(if(contains(str(?voting),"ep2019"),?voters,0) as ?ep2019)
    bind(if(contains(str(?voting),"mi2019/os"),?voters,0) as ?mi2019)

    ?sec myd:place ?place . 
    ?place rdfs:label ?place_label ; myd:population ?pop ; myd:municipality ?mun .
    ?mun rdfs:label ?mun_label 
    bind(strafter(str(?place),str(place:)) as ?ekatte) 
} 
group by ?mun_label ?place_label ?ekatte ?pop
```

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

### Coordinates based on WKT

```spaqrl
PREFIX sf: <http://www.opengis.net/ont/sf#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
insert {
    graph <https://elections.ontotext.com/resource/graph/geo-test> {
    ?point geo:lat ?lat ;
           geo:long ?lon .
	}
} where {
	?point a geo:Geometry ; geo:asWKT ?wkt .
    bind(xsd:float(replace(strafter(str(?wkt),"Point(")," .*","")) as ?lon)
    bind(xsd:float(replace(strafter(str(?wkt),"Point("),"([0-9]|\\.)* |\\)","")) as ?lat)
};
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

# Dump and export

All votes for a selection of main parties

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?voting ?round ?date (sample(?el_label) as ?EL_LABEL) ?sec_num ?sec_address ?place ?place_label ?party_label ?main_party_label (sum(?n_votes) as ?VOTES) ?total_votes ?prot where { 
    values ?main_party {
       wd:Q164242  #DPS
       wd:Q133968 #GERB,
       wd:Q792527 #VMRO,
       wd:Q283129 #Zelenite,
       wd:Q841253 #SDS,
     [analysis_11_21_pivot.xlsx](akf%2Fkkvot22%2Fanalysis_11_21_pivot.xlsx)  wd:Q62808154 #db,
       wd:Q97387007 #NFSB-ep,
       wd:Q971439 #Koalicia za Bulgaria,
       wd:Q97395772 #Nova republika,
       wd:Q31191941 #DaBG,
       wd:Q97382346 #OP,
       wd:Q97396346 #RB2017,
       wd:Q15991304 #RB,
       wd:Q178049 #Ataka,
       wd:Q752259 #BSP       
}
    
    ?party rdfs:label ?party_label ; myd:party+ ?main_party .	
	?main_party rdfs:label ?main_party_label .
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el ;
         myd:number ?sec_num ;
    .
    ?el myd:main_election election:mi2015 . #FILTER ELECTIONS HERE
    
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes ;
        	myd:vote ?party ;
         	myd:link_html ?prot ;
            myd:date ?date ;
    .		
    optional {?voting myd:round ?round}
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?n_votes.
    
    optional {
        ?sec myd:votingPlace ?voting_place .
        ?voting_place rdfs:label ?sec_address .
    }
    
    ?el rdfs:label ?el_label .
    ?place rdfs:label ?place_label .
} group by ?voting ?round ?date ?sec_num ?sec_address ?place ?place_label ?party_label ?main_party_label ?total_votes ?prot
```

