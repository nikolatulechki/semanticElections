# SOFIA PROFILING

Compute arbitrary rule based counts at the polling station level
Each query observations to the `<cube/sofia-profiling>` cube in a separate graph

## PPDB-core

Voted for PPDB in  pi2023

## GERB-core

MIN voted GERB

## UNVOTEd-core

min(voters-voted)

## CSV download

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@results_drilldown.rq' 'https://elections.ontotext.com/repositories/elections' > data/sofia_cores.csv
```