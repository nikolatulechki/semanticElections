```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@top_cands.rq' 'https://elections.ontotext.com/repositories/elections' > data/top_cands.csv
```