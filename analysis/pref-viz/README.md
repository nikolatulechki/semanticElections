# Preference plots

```sparql
# pref votes per party and per election

BASE  <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
select ?name ?cand_number_norm ?mir (sum(?pref) as ?pref_votes) where { 

#    bind(wd:Q164242 as ?party) #DPS
    bind(wd:Q133968 as ?party) #ГЕРБ
    bind(<election/pi2021> as ?main_el) #"Избори за Европейски Парламент 2019"
    ?candidate a my:Candidate ; myd:represents ?localParty  ; myd:candidacy ?el ; rdfs:label ?name ; myd:number ?cand_number .
    ?localParty  myd:party/myd:party ?party ; myd:number ?party_number .
    ?el myd:main_election ?main_el ; myd:jurisdiction/myd:number ?mir .
    ?pv myps:preference_vote ?candidate ; mypq:valid_votes_recieved ?pref .
    bind(if(xsd:integer(?cand_number)>100,xsd:integer(?cand_number)-100,?cand_number) as ?cand_number_norm)
} group by ?name ?cand_number_norm ?mir order by ?mir
```