# Mandate distribution simulations

We use BIRD's mandate calculator. The following queries generate input following 

<https://bird.bg/izbori2021/index.html>

Reformat csv:
```shell
csvformat -D=";" -K 1  pi2017_actual.csv  > pi2017_actual_ok.csv
```

## Actual results 

```sparql
# Baseline results per MIR
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?mir ?partyName (sum(?valid_votes) as ?sum_valid_votes) 
where {
    bind(<election/pi2017> as ?election) 
    ?party a my:ElectionParty ;
           rdfs:label ?partyName .
    ?voting myp:vote ?vote  ;
            myd:main_election ?election ;
            myd:election/myd:jurisdiction/myd:number ?mir ;
                                         myd:section ?sec ;
                                         .
    ?vote myps:vote/myd:party ?party;
                   mypq:valid_votes_recieved ?valid_votes ;
                   .
} group by ?mir ?partyName order by ?mir ?partyName
```

## None votes 

### In high-risk sections

### In potential-risk sections

```sparql
# Baseline results per MIR
BASE <https://elections.ontotext.com/resource/>
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX election: <https://elections.ontotext.com/resource/election/>
select ?mir ?partyName (sum(?valid_votes) as ?sum_valid_votes) 
where {
    bind(<election/pi2017> as ?election) 
    ?party a my:ElectionParty ;
           rdfs:label ?partyName .
    ?voting myp:vote ?vote  ;
            myd:main_election ?election ;
            myd:election/myd:jurisdiction/myd:number ?mir ;
            myd:section ?sec ;
                                         .
    ?vote myps:vote/myd:party ?party;
                   mypq:valid_votes_recieved ?valid_votes ;
                   .
    filter not exists {
        ?sec myd:meta_section ?ms .
        ?ms myd:risky_model [] .
    }
} group by ?mir ?partyName order by ?mir ?partyName
```

https://www.capital.bg/politika_i_ikonomika/bulgaria/2021/04/06/4195043_300_lv_i_5_greshnite_smetki_i_realnata_tejest_na/