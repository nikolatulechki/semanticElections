# semanticElections
RDF-ization of Bulgarian election results

# Data Anаlysis 

## Section sheet

get section [sheet](https://docs.google.com/spreadsheets/d/1ntQtECbUTI_LlEQMTvNuXSKj_wiSWCv0QPBTGAUGgnM/) 

```bash
curl "https://docs.google.com/spreadsheets/d/1ntQtECbUTI_LlEQMTvNuXSKj_wiSWCv0QPBTGAUGgnM/gviz/tq?tqx=out:csv" -o Sekcii.csv
```

header: 
1. SECID
1. Област код (OBL)
1. Област текст 
1. Община код (OBS)
1. Община
1. Район код (REG)
1. Район
1. Секция (SEC)
1. Населено място код
1. Населено място
1. Адрес


```
 % csvcut -c 9,10  Sekcii.csv | sort -u | wc -l
7555
```
7555 unique locations to run through google api 

## List of parties 

<https://www.cik.bg/bg/mi2019/registers/parties>

## CIK protocols access

section ID is formed from concatenating OBL,OBS,REG,SEC of the sections sheet

CIK publishes at most 4 protocols in 2 formats each:
example:
<https://results.cik.bg/mi2019/tur1/protokoli/2/2246/224621001.html>
structure

* prefix: `https://results.cik.bg/mi2019/`
* elections: `mi2019/`
* round: `tur1/`
* format
    * `protokoli/` - digital 
    * `pdf/ - scanned 
* type of protocol
    * Кмет на община `2/`
    * Общински съвет `1/`
    * Кмет на кметство `4/`
    * Кмет на район  `8/`
* bucket `OBL+OBS/`
* section ID 
* extension 
    * `.html` - machine readable
    * `.pdf` - scanned version 
hh

example:                                                             
<https://results.cik.bg/mi2019/tur1/protokoli/2/2246/224621001.html> 
<https://results.cik.bg/mi2019/tur1/pdf/2/2246/224621001.pdf> 

Протокол за избор на кмет на община в Доброславци, софииско

# Google sheet parsing 

Ready sheets:

[Slatina](https://docs.google.com/spreadsheets/d/1CLUconDxMbylYj6ngwKQDy-sN7z_XFyUDdopSma-vdk)
[Krasna Polqna](https://docs.google.com/spreadsheets/d/1zGE-mPMEfhSrFz3SxdM7w2vynHiKfNuHTB1qm4FmL2g) 
[Sliven](https://docs.google.com/spreadsheets/d/10WHjtcKxTXaomKDmDdwKrhxwVQLRKY8uGw4cu8551w0)

## Import function in GS

`=query({IMPORTHTML(CONCATENATE("https://results.cik.bg/mi2019/tur1/protokoli/2/2246/224611",B1,".html"),"table",5)},"select Col2",1)`

# CIK open data

No new sections created at second round 
`diff ../tur2/ko/sections_03.11.2019.txt ../tur1/ko/sections_27.10.2019.txt | grep "<"`

Remove unbalanced quotes

`sed -i "s/[\"\„\“]//g" ../tur1/ko/local_candidates_27.10.2019.txt` 
`sed -i "s/[\"\„\“]//g" ../tur2/ko/local_candidates_03.11.2019.txt` 
`sed -i "s/[\"\„\“]//g" ../tur1/os/local_candidates_27.10.2019.txt`
`sed -i "s/[\"\„\“]//g" ../tur1/ko/local_parties_27.10.2019.txt`


```
sed -i "s/Местна коалиция Движение ЗАЕДНО за промяна (Коалиция Движение ЗАЕДНО за промяна; ПП ЕДИННА НАРОДНА ПАРТИЯ; ПП ДВИЖЕНИЕ ГЕРГЬОВДЕН; ПП СЪЮЗ НА СВОБОДНИТЕ ДЕМОКРАТИ; ПП ДВИЖЕНИЕ БЪЛГАРИЯ НА ГРАЖДАНИТЕ; ПП БЪЛГАРСКИ ЗЕМЕДЕЛСКИ НАРОДЕН СЪЮЗ; ПП СЪЮЗ НА ДЕМОКРАТИЧНИТЕ СИЛИ)/Местна коалиция Движение ЗАЕДНО за промяна (Коалиция Движение ЗАЕДНО за промяна, ПП ЕДИННА НАРОДНА ПАРТИЯ, ПП ДВИЖЕНИЕ ГЕРГЬОВДЕН, ПП СЪЮЗ НА СВОБОДНИТЕ ДЕМОКРАТИ, ПП ДВИЖЕНИЕ БЪЛГАРИЯ НА ГРАЖДАНИТЕ, ПП БЪЛГАРСКИ ЗЕМЕДЕЛСКИ НАРОДЕН СЪЮЗ, ПП СЪЮЗ НА ДЕМОКРАТИЧНИТЕ СИЛИ)/g" ../tur1/os/local_candidates_27.10.2019.txt
```

Query to clean-up broken labels 
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
delete {?s rdfs:label ?label}
#select *
where { 
    ?s rdfs:label ?label .
    filter(contains(?label,"��"))
    {select ?s (count(*) as ?c) where {
        ?s rdfs:label ?label . 
        } group by ?s having(?c>1) }
} 
```

Всички кандидати на ДАБГ
```
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
select ?cand ?election ?name ?elLabel ?round {
    ?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents <party/66> .
    ?election rdfs:label ?elLabel .
    optional {?election myd:round ?round .}
}
```

Candidates on tur 1 with aggregated votes

```sparql
BASE <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX myp: <https://github.com/nikolatulechki/semanticElections/resource/prop/indirect/>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
select ?election ?party ?cand ?name (sum(?votes) as ?sum_votes)
where { 
#bind(<https://github.com/nikolatulechki/semanticElections/resource/entity/election/mi2019/ko/0101/tur1> as ?election)
?cand a my:Candidate ; myd:candidacy ?election ; rdfs:label ?name ; myp:candidacy/mypq:represents ?party .
?election myd:round 1 .
?voting myd:partOf ?election . 
?s ^myp:vote ?voting ; myps:vote ?party ; mypq:valid_votes_recieved ?votes .     
} group by ?election ?party ?cand ?name order by desc(?sum_votes)
```

## Местни Коалиции 

fix double party types 
```
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
delete {
    ?party myd:type "independant" } 
where { 
    ?party a my:Party ; myd:type "local_coalition" .
}
```

Gen Coalitions (temp)

```sparql
PREFIX my: <https://github.com/nikolatulechki/semanticElections/resource/entity/>
PREFIX myd: <https://github.com/nikolatulechki/semanticElections/resource/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mypq: <https://github.com/nikolatulechki/semanticElections/resource/prop/qualifier/>
PREFIX myps: <https://github.com/nikolatulechki/semanticElections/resource/prop/statement/>
select 

?party ?municipality ?name (group_concat(distinct ?el_notation;separator=";") as ?elections) 
where { 
    ?party a my:Party ; 
        myd:type "independant" ; 
        rdfs:label ?name ;
        ^mypq:represents/myps:candidacy ?cand ;
    .
    ?cand myd:municipality/rdfs:label ?municipality ; myd:partOf ?election .
    bind(strafter(str(?election),concat(str(my:),"election/mi2019/")) as ?el_notation) 
    
} 
group by ?party ?municipality ?name 
```