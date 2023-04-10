Result [gsheet](https://drive.google.com/drive/u/1/folders/1pbrwJiWBRGKRlhIzsA1SwQSfmmsY1phA)

`^.*\– `

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_section.rq' 'https://elections.ontotext.com/repositories/elections' > out/dif_section.csv
```

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_section_missing_votes.rq' 'https://elections.ontotext.com/repositories/elections' > out/dif_section_missing_votes.csv
```

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_mun.rq' 'https://elections.ontotext.com/repositories/elections' > out/dif_mun.csv
```