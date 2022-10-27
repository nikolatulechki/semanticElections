# Semantic Elections

This project's goal is to convert CIK open data about bulgarian elections to 5-star RDF. If you don't already know why this is useful, read this [blog post](https://www.ontotext.com/blog/5-star-linked-open-elections-data/).

## Endpoint

 The sparql endpoint is situated at <https://elections.ontotext.com>

## Data Model

Example diagrams in the [model](./model) folder. 

## Example SPARQL Queries 

### Търся Кандидат по (част от) името 

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select * where { 
	?s a my:Candidate ; rdfs:label ?lab ; myd:candidacy ?el .
    optional{?el rdfs:label ?elLabel }
    filter(contains(lcase(?lab),"марешк"))
} 
```

### Всички известни партии 
```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select * where { 
	?s a my:Party ; rdfs:label ?label 
} order by ?label
```

### Всички избори в които дадена партия е участвала

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select * where { 
    bind(wd:Q164242 as ?party) #DPS
	?party rdfs:label ?lab .
    ?electionParty myd:party ?party ; myd:candidacy ?election ; myd:number ?ballot_num .
    ?election myd:date ?date .
    optional{ ?election rdfs:label ?label .}
} order by desc(?date)
```
### Партии и коалиции на местно ниво отнасящи се към дадена партия 

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?localParty ?localPartyLabel ?ballotNum ?localEl ?localElLabel ?munLabel where { 
#    bind(wd:Q164242 as ?party) #DPS
    bind(wd:Q792527 as ?party) #VMRO
    
    bind(election:mi2015 as ?election) #LOCAL 2015, use mi2019 for local 2019
	?party rdfs:label ?lab .	
    ?electionParty myd:party ?party ; myd:candidacy ?election ; myd:number ?num .
    ?localParty a my:LocalParty ; myd:party ?electionParty ; rdfs:label ?localPartyLabel ; myd:number ?ballotNum ; myd:candidacy ?localEl .
    ?localEl rdfs:label ?localElLabel ; myd:jurisdiction ?mun. 
    ?mun rdfs:label ?munLabel .
}
```

### Листата на дадена партия за даден избор 

```sparql
BASE  <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?localEl ?localElLabel ?mirNumber ?localParty ?localPartyLabel ?localPartyNumber ?candidate ?candNumber ?name   where { 

    bind(wd:Q164242 as ?party) #DPS
    #bind(wd:Q792527 as ?party) #VMRO
    
#    bind(<election/mi2015/os/1910> as ?localEl) #"Местни Избори 2015 за общински съвет 1910. Дулово"
    bind(<election/pi2017/24> as ?localEl) #"Избори за Парламент на РБ МИР  24. СОФИЯ 24 МИР"
#    bind(<election/ep2019> as ?localEl) #"Избори за Европейски Парламент 2019"
    
    ?localParty  myd:party+ ?party ; rdfs:label ?localPartyLabel ; myd:number ?localPartyNumber ; myd:candidacy ?localEl .
    ?candidate a my:Candidate ; myd:represents ?localParty  ; rdfs:label ?name ; myd:number ?candNumber .
    
    ?localEl rdfs:label ?localElLabel ; 
    optional{?localEl myd:jurisdiction/myd:number ?mirNumber}
} order by ?candNumber 
```

### Aggregated results on municipality level (local election results)

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?candidate ?name ?party ?partyName (sum(?valid_votes) as ?sum_valid_votes) (sum(?invalid_votes) as ?sum_invalid_votes) 
    where {
    	bind(<election/mi2019/ko/tur1/2246> as ?election) #"Местни Избори 2019 за кмет на община 2246. Столична - Тур 1"
        ?party a my:LocalParty ;
              #myd:candidacy ?election ;
              rdfs:label ?partyName .
        ?voting myp:vote ?vote  ;
                myd:election ?election .
    	?candidate a my:Candidate ;
                myd:represents ?party ; 
                myd:candidacy ?election ; 
                rdfs:label ?name ;
         .
        ?vote myps:vote ?party;
            mypq:valid_votes_recieved ?valid_votes ;
            mypq:invalid_votes_recieved ?invalid_votes .
     } 
group by ?election ?party ?partyName ?candidate ?name order by desc(?sum_valid_votes)
```
### Агрегирани резултати по населено място 

```sparql
# Агрегирани резултати по населено място 
# Агрегирани резултати по населено място 

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select

?place_label ?date ?el ?el_label ?party_label (sum(?n_votes) as ?sum_votes) ?sum_voted (floor(?sum_votes/?sum_voted*10000)/100 as ?ratio)
where {
    
    bind(place:22530 as ?place) # place:EKATTE 
    
    {select distinct ?el ?place (sum(?voted) as ?sum_voted) {
       ?sec a  my:Section ;
         myd:place ?place ;
         myd:election ?el .
    ?voting myd:section ?sec ;
            myd:voters_voted_count ?voted ;
    } group by ?el ?place }
    
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el .
    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
    		myd:voters_voted_count ?voted ;
     .
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?n_votes ;
    .
    filter(?n_votes > 10)
    ?party rdfs:label ?party_label .
    ?el rdfs:label ?el_label ; myd:date ?date . 
    ?place rdfs:label ?place_label .
} group by ?date ?place_label ?el ?el_label ?party_label ?sum_voted order by desc(?date) ?el desc(?sum_votes)
```
### всички резултати на дадена партия, агрегирани по населено място, за определен избор (в случая - за ДПС за изборите за общински съветници 2019

```spaqrl
BASE  <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX wd: <http://www.wikidata.org/entity/>

select ?place ?place_label ?el_label ?el ?party ?party_label (sum(?n_votes) as ?sum_votes) where {
    
 	?el myd:partOf	<election/mi2019/os> . #use <election/mi2019/os> for 2015 municipal council elections 
    ?party myd:party/myd:party wd:Q164242 . # gerb is wd:Q133968
        
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el .
    ?voting myd:section ?sec ;
            myp:vote ?vote_st .
    ?vote_st myps:vote ?party ;
             mypq:valid_votes_recieved ?n_votes.
    ?party rdfs:label ?party_label .
    ?el rdfs:label ?el_label .
    ?place rdfs:label ?place_label .
} group by ?place ?place_label ?el ?el_label ?party ?party_label order by ?el
```

### Вот по секции за даден набор партии в дадено населено място 

```sparql
# Вот по секции за даден набор партии в дадено населено място 

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX wd: <http://www.wikidata.org/entity/>
select ?voting ?el_label ?sec_num ?vote_type ?party_label ?n_votes  ?total_votes ?vote_ratio ?prot_html ?prot_pdf { 
    values ?main_party {
        wd:Q164242  #DPS
        wd:Q133968 #GERB  
    }
    bind(place:37376 as ?place) # place:EKATTE 
    ?sec a  my:Section ;
         myd:place ?place ;
         rdfs:label ?section_label ;
         myd:election ?el ;
         myd:number ?sec_num ;
    .
	?party rdfs:label ?party_label ; myd:party+ ?main_party .

    ?voting myd:section ?sec ;
            myp:vote ?vote_st ;
            myd:voters_voted_count ?total_votes ;
    		myd:link_pdf ?prot_pdf ;
      		myd:link_html ?prot_html ;
        	myd:vote ?party ;
    .		
    ?vote_st myps:vote ?party ;
             mypq:type ?vote_type ;
             mypq:valid_votes_recieved ?n_votes.
    bind(floor((?n_votes/?total_votes)*10000)/100 as ?vote_ratio)
    ?el rdfs:label ?el_label .
    ?place rdfs:label ?place_label .
} order by ?el ?sec_num
```

### Peevski's preferences

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select * {
	
    {select * where { 
            ?cand a my:Candidate ; rdfs:label ?lab ; myd:candidacy ?el .
            optional{?el rdfs:label ?elLabel }
            filter(contains(lcase(?lab),"делян славчев пеевски"))
    }}
    ?voting myp:preference_vote ?pv ; myd:election ?el.
    ?pv myps:preference_vote ?cand ; mypq:valid_votes_recieved ?pref .
    filter(?pref > 10)
} 
```

### Преференциите на даден кандидат с географски сечения и относителен резултат

```sparql
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
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select ?election ?election_date ?party_label ?cand_number ?cand_name ?obl ?mun ?place ?sec_id ?cand_preferences ?party_votes ?pref_ratio ?total_voted ?party_ratio ?protocol where {


    {select ?candidate where {
            ?candidate a my:Candidate ; rdfs:label ?lab ; myd:candidacy ?el .
            optional{?el rdfs:label ?elLabel }
            filter(contains(lcase(?lab),"мартин николаев харизанов"))
    }}

    ?candidate a my:Candidate ; myd:represents ?localParty  ; myd:candidacy ?el ; rdfs:label ?cand_name ; myd:number ?cand_number .
    ?voting  myp:vote ?v ;  myd:section ?section ; myd:link_html ?protocol ; myd:voters_voted_count ?total_voted .
    ?el myd:main_election ?election ; myd:date ?election_date ; myd:jurisdiction jurisdiction:6 .
    ?v myps:vote ?localParty ; mypq:valid_votes_recieved ?party_votes .
        optional{?voting myp:preference_vote ?pv .
        ?pv myps:preference_vote ?candidate ; mypq:valid_votes_recieved ?cand_preferences .
    }
    ?localParty rdfs:label ?party_label .
    ?section myd:number ?sec_id ;
             myd:place/rdfs:label ?place ;
             myd:place/myd:municipality/rdfs:label ?mun ;
             myd:place/myd:municipality/myd:province/rdfs:label ?obl ;
    .

    bind(floor((?cand_preferences/?party_votes)*10000)/100 as ?pref_ratio)
    bind(floor((?party_votes/?total_voted)*10000)/100 as ?party_ratio)

} order by desc(?election_date)
```

### Изборните секции в Драгичево

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX place: <https://elections.ontotext.com/resource/place/>
select * where { 
	?s a  my:Section ; myd:place place:23251 ; rdfs:label ?label ; myd:election ?el .
    ?el rdfs:label ?elLabel .
} limit 100 
```