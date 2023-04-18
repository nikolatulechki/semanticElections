Result [gsheet](https://drive.google.com/drive/u/1/folders/1pbrwJiWBRGKRlhIzsA1SwQSfmmsY1phA)

`^.*\– `

#SECTION 
```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_section.rq' 'https://elections.ontotext.com/repositories/elections' > data/dif_section.csv
```

# PLACE
```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_place.rq' 'https://elections.ontotext.com/repositories/elections' > data/dif_place.csv
```

# MUN
```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_mun.rq' 'https://elections.ontotext.com/repositories/elections' > data/dif_mun.csv
```

# MIR
```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_mir.rq' 'https://elections.ontotext.com/repositories/elections' > data/dif_mir.csv
```

```bash
curl -X POST -H 'Content-Type:application/sparql-query' -H 'Accept: text/csv' --data-binary '@dif_place.rq' 'https://elections.ontotext.com/repositories/elections' > data/dif_place.csv
```