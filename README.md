# Semantic Elections

This project's goal is to convert CIK open data about bulgarian elections to 5-star RDF 

## Endpoint

 The sparql endpont is situated at <https://elections.ontotext.com>

## Data Model

Example diagrams in the [model](./model) folder. 

## Example SPARQL Queries 

### Търся Кандидат 

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
### Всички избори в които дадена партия е участвала

```
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select * where { 
    bind(wd:Q164242 as ?party) #DPS
	?party rdfs:label ?lab .
    ?electionParty myd:party ?party ; myd:candidacy ?election ; myd:number ?num .
    optional{ ?election rdfs:label ?label .}
}
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

### Партии и коалиции на местно ниво отансящи се към дадена партия

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?localParty ?localPartyLabel ?localNum ?localEl ?localElLabel where { 
    #bind(wd:Q164242 as ?party) #DPS
    bind(wd:Q792527 as ?party) #VMRO
    
    bind(election:mi2015 as ?election) #LOCAL 2015, use mi2019 for local 2019
	?party rdfs:label ?lab .
    ?electionParty myd:party ?party ; myd:candidacy ?election ; myd:number ?num .
    ?localParty a my:LocalParty ; myd:party ?electionParty ; rdfs:label ?localPartyLabel ; myd:number ?localNum ; myd:candidacy ?localEl .
    ?localEl rdfs:label ?localElLabel .
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
select ?candidate ?candNumber ?name ?localParty ?localPartyLabel ?localPartyNumber ?localEl ?localElLabel where { 

    bind(wd:Q164242 as ?party) #DPS
    #bind(wd:Q792527 as ?party) #VMRO
    
#    bind(<election/mi2015/os/1910> as ?localEl) #"Местни Избори 2015 за общински съвет 1910. Дулово"
#    bind(<election/pi2017/24> as ?localEl) #"Избори за Парламент на РБ МИР  24. СОФИЯ 24 МИР"
#    bind(<election/ep2019> as ?localEl) #"Местни Избори 2015 за общински съвет 1910. Дулово"
    
    ?localParty  myd:party+ ?party ; rdfs:label ?localPartyLabel ; myd:number ?localPartyNumber ; myd:candidacy ?localEl .
    ?candidate a my:Candidate ; myd:represents ?localParty  ; rdfs:label ?name ; myd:number ?candNumber .
    
    ?localEl rdfs:label ?localElLabel .
} order by ?candNumber 
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
