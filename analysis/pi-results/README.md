# Computing of parliamentary election mandates

## Objective 
Generate automatically parliamentary election final results (mandate distribution) from section-level data 

## Motivation
We want to be able to write rules with SPARQL and simulate different outcomes in certain sections. Once these results are generated, we want to run a procedure which outputs the final composition of the national assembly under those conditions .

## Mandate distribution methodology

* [Paper](https://ejournal.vfu.bg/en/pdfs/Zdravko_Slavov_Matematicheski_Metodi_za_Razpredelenie_na_Mandatite.pdf>) on proportional voting systems (in Bulgarian).
* TLDR; here they use the [Hare quota](https://en.wikipedia.org/wiki/Hare_quota) system
* CIK overall results for pi2017: <https://results.cik.bg/pi2017/mandati/index.html>
* CIK results granular tables per MIR with remainders for pi2017 <https://results.cik.bg/pi2017/hnm.html>

## Queries aggregating section level data

### Total vote counts per MIR (table 1)

```sparql
 BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select 
?mir  (sum(?section_votes) as ?votes)
where {
    bind(<election/pi2017> as ?main_election) 
    ?voting myd:main_election ?main_election ;
            myd:election/myd:jurisdiction ?mir ;
            myd:votes_valid_count ?section_votes ;
    .
} group by ?mir order by ?mir
```

### Aggregated votes per MIR (table 2)

```sparql
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select 
?mir ?party_number ?party_label (sum(?section_votes) as ?votes)
where {
    bind(<election/pi2017> as ?main_election) 
    ?voting myp:vote ?vote  ;
            myd:main_election ?main_election ;
            myd:election/myd:jurisdiction ?mir ;
                        .
    ?vote myps:vote ?local_party;
          mypq:valid_votes_recieved ?section_votes .
    ?local_party a my:LocalParty ;
                 myd:party ?election_party .
    ?election_party rdfs:label ?party_label ;
                    myd:number ?party_number ;
                    .
} group by ?mir ?party_number ?party_label order by ?mir ?party_number
```


