# Model

## Relevant WD types and props 

* Candidate (Q5)
* Political Party 
** Political party in Bulgaria Q43791339
** Political party (Q7278)
* Election (Q40231) 
* Polling place [Q335778](http://www.wikidata.org/entity/Q335778)
* Facility (school, community center, see restraints on polling place)
* electoral list 
    * candidacy within an electoral list see [here](https://www.wikidata.org/wiki/Q64018521#Q64018521$ce947c88-46f7-c591-a7b1-7ec8453387af)
    * election employing electoral lists: [Q64017516](https://www.wikidata.org/wiki/Q64017516) 
* Office Contested P541, [query](https://w.wiki/BWr) for instances of Offices
    * Mayor Of Kmetstvo
    * Mayor Of Municipality
    * Councillor at council of Municipality
    * Mayor of District


## Election Entities 

People Voluyak voted on 4 separate elections 

* Local Mayor Elections  - voting for mayor of Voluyak itself 
* Municipal Council elections - Voting for council of Sofia Capital Municipality [Q4442915](http://www.wikidata.org/entity/Q4442915) 
* Municipal Mayor elections -  

### Local vs Naitonal enitites

* National enities are accesisble at the CIK portal. They are identifieble by the same number 
* Loacal entites are available at OIK sub portals as shitty doc files. Probably it will be eaiser to extract them directly from the protocols
* Lists of candidates...
    *Result tables for councellors https://results.cik.bg/mi2019/tur1/hnm/0101.html

### Wiki Project Elections

<https://www.wikidata.org/wiki/Wikidata:WikiProject_elections> 

### Girona 2015 municipal election model 

see election.ttl

Elections where "convergence and Union" participated 
```sparql
select ?election ?electionLabel {
  ?election wdt:P726 wd:Q150398 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```



### Voting process

Q189760 voting is a good type 

TODO Still looking how represent sections

[Individual Constituency Budapest No. 15](https://www.wikidata.org/wiki/Q15728580) example of constituency.. but this corresponds more to a МИР

[Wiki](https://bg.wikipedia.org/wiki/Избирателни_райони_в_България#Избирателни_комисии) about voting comissions in BG




## Queries 

```sparql 
BASE <https://github.com/nikolatulechki/semanticElections/resource/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/anentity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
select ?name ?elLabel {
    ?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents <party/43> .
    ?election myd:round 2 ; rdfs:label ?elLabel .
```


## Bulgarian entities on Wikidata

### Geography 

Working on elections at Волуяк 

EKATTE : 12084 - (wdt:P3990) 
WD concept <http://www.wikidata.org/entity/Q2455639>
Voluyak is a kmetstvo (Q4224624)

Query for BG territorial entities:

They voted in 3 separate polling places [Q335778](http://www.wikidata.org/entity/Q335778)

* 224620049
* 224620050
* 224620051

All use the same facility (School) - "146 ОУ "Патриарх Евтимий", ул. Зорница № 63" С.ВОЛУЯК"    

```sparql
select ?s ?sLabel ?ekatte {
  ?s wdt:P3990  ?ekatte .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,bg". }
}
```
[query](https://w.wiki/BuT)

### People 

11833 Bulgarians on wikidata 

```sparql
select ?s ?sLabel  {
  ?s wdt:P31 wd:Q5 ; wdt:P27 wd:Q219  .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,bg". }
}
```
[query](https://w.wiki/BuV)

### Political Parties

Relevant type [Q43791339](http://www.wikidata.org/entity/Q43791339) : political party in Bulgaria

61 parites in BG: [query](https://w.wiki/BuY)


## Person matching 
he same municipality and the same party 
After obvious matching of homoyms and dedupliction within the context of the the same party and the same municipality we still have 400 clusters of homonyms...

Decision is to import them as is. 

```
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX onto: <http://www.ontotext.com/>
select
?l (count(*) as ?c)  
from onto:disable-sameAs
where { 
    ?c1 a my:Candidate ; rdfs:label ?l .
    ?c2 a my:Candidate ; rdfs:label ?l .
    
    filter(str(?c1)>str(?c2))
    
}
group by ?l order by desc(?c)
``` 


## Craeting Wikidata entities

Query to make Position instances
```sparql
select ?PosBgLabel ?PosEnLabel ?q {
  ?m wdt:P31 wd:Q1906268
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "bg". 
    ?m rdfs:label ?mBgLabel
  }
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "en". 
    ?m rdfs:label ?mEnLabel
  }
  bind(strafter(str(?m),str(wd:)) as ?q)
  bind(concat("Mayor of ",?mEnLabel) as ?PosEnLabel)
  bind(concat("Кмет на ",?mBgLabel) as ?PosBgLabel) 
}
```


generating labels fr coalitions 

```
select ?Q ?Dbg ?cdescription  {
  ?s wdt:P31 wd:Q388602 ; wdt:P2541 ?mun .
  ?mun wdt:P31 wd:Q1906268 ; 
  SERVICE wikibase:label { 
    bd:serviceParam wikibase:language "bg". 
    ?s rdfs:label ?sLabel .
    ?mun rdfs:label ?munLabel .
  }
  bind(strafter(str(?s),str(wd:)) as ?Q)
  bind(concat(?sLabel, " - Местни Избори 2019 - ",?munLabel) as ?cdescription)
  bind("Dbg" as ?Dbg)
  
}
``` 