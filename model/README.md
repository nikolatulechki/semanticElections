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

## Geography 

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
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
select ?name ?elLabel {
    ?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents <party/43> .
    ?election myd:round 2 ; rdfs:label ?elLabel .
```








