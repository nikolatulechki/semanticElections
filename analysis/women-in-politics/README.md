# Women in politics

[GFolder](https://drive.google.com/drive/u/2/folders/164h7qGR1MdHmHaZkNkRwltotltDZLy3Y)

## Gender balance in elections candidates

Endpoint to use: <https://elections.ontotext.com/repositoeries/elections> ([Web](https://elections.ontotext.com/))

Какво е процентното съотношение на жените и мъжете в кандидатските листи 
на парламентарно представените партии и коалиции в периода 2013-2023?

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
BASE <https://elections.ontotext.com/resource/>

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select
?party_label ?el_party_label ?date ?mir_label ?mir_num ?el_label (sum(?M) as ?males) (sum(?F) as ?females)
where {

    values (?party ?party_label) {
        (wd:Q164242    "dps")
        (wd:Q792527    "vmro")
        (wd:Q108601789 "pp")
        (wd:Q28943121  "vuz")
        (wd:Q98098908  "itn")
        (wd:Q133968    "gerb")
        (wd:Q62808154  "db")
        (wd:Q752259    "bsp")
        (wd:Q25485773  "volya")
        (wd:Q97396346  "rb")
        (wd:Q15991304  "rb")
        (wd:Q97382346  "patr")
        (wd:Q17514144  "patr")
        (wd:Q178049    "ataka")
        (wd:Q106393525    "ismv")
        (wd:Q74877838  "bno")
        (wd:Q104203765  "rep")
    }

    ?c a my:Candidate ; 
       myd:represents ?election_party ;
       myd:candidacy ?el ;
       myd:sex ?sex .
    ?election_party myd:party* ?party ;
       rdfs:label ?el_party_label ;
       myd:number ?ballot_num ;
    .
    ?el myd:jurisdiction ?mir ; myd:date ?date ; myd:main_election/rdfs:label ?el_label .
    ?mir rdfs:label ?mir_label ; myd:number ?mir_num .
    bind(if(?sex="male",1,0) as ?M)
    bind(if(?sex="male",0,1) as ?F)
} 
group by ?party_label ?el_party_label ?date ?mir_label ?mir_num ?el_label
order by desc(?date) ?party_label ?mir_num 
```

Какъв е процентът на жените водачи в кандидатските листи 
на парламентарно представените партии и коалиции в периода 2013-2023?

```sparql
PREFIX wd: <http://www.wikidata.org/entity/>
BASE <https://elections.ontotext.com/resource/>

PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
PREFIX myp: <https://elections.ontotext.com/resource/prop/indirect/>
PREFIX mypq: <https://elections.ontotext.com/resource/prop/qualifier/>
PREFIX myps: <https://elections.ontotext.com/resource/prop/statement/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX election: <https://elections.ontotext.com/resource/election/>
PREFIX jurisdiction: <https://elections.ontotext.com/resource/jurisdiction/>
select 
?party_label ?date ?el_label (sum(?M) as ?males) (sum(?F) as ?females)
where {

    values (?party ?party_label) {
        (wd:Q164242    "dps")
        (wd:Q792527    "vmro")
        (wd:Q108601789 "pp")
        (wd:Q28943121  "vuz")
        (wd:Q98098908  "itn")
        (wd:Q133968    "gerb")
        (wd:Q62808154  "db")
        (wd:Q752259    "bsp")
        (wd:Q25485773  "volya")
        (wd:Q97396346  "rb")
        (wd:Q15991304  "rb")
        (wd:Q97382346  "patr")
        (wd:Q17514144  "patr")
        (wd:Q178049    "ataka")
        (wd:Q106393525    "ismv")
        (wd:Q74877838  "bno")
        (wd:Q104203765  "rep")
    }

    ?c a my:Candidate ; 
       myd:represents ?election_party ;
       myd:candidacy ?el ;
       myd:sex ?sex ;
       myd:number ?number ;
    .
    filter(?number=1 || ?number=101)
    ?election_party myd:party* ?party ;
       rdfs:label ?el_party_label ;
       myd:number ?ballot_num ;
    .
    ?el myd:jurisdiction ?mir ; myd:date ?date ; myd:main_election/rdfs:label ?el_label .
    ?mir rdfs:label ?mir_label ; myd:number ?mir_num .
    bind(if(?sex="male",1,0) as ?M)
    bind(if(?sex="male",0,1) as ?F)
} 
group by ?party_label ?date ?el_label
order by desc(?date) ?party_label 
```
## Gender balance of MPs in national assembly

Какво е процентното съотношение на жените и мъжете в Народното събрание в периода 1990-2023?
(ако е възможно да се покаже и разпределението по партии/коалиции и избирателни райони)

### Grouped by NS

Endpoint to use: <https://query.wikidata.org/sppaqrl> ([Web](https://query.wikidata.org/))

```sparql
select 
 ?nsLabel ?NUM  (sum(?M) as ?males) (sum(?F) as ?females) 
{
  {select ?x ?ns ?NUM ?sex {
    ?ns p:P31 [ps:P31 wd:Q43792361 ; pq:P1545 ?num] 
    bind(strdt(?num,xsd:integer) as ?NUM)    
    filter(?NUM >= 39)     
    ?x p:P39 [ps:P39 wd:Q18924508 ; pq:P2937 ?ns ; pq:P768 ?mir ; pq:P4100 ?pg] ; wdt:P21 ?sex .
    ?mir p:P31/pq:P1545 ?mir_num .
  } group by ?x ?ns ?NUM ?sex }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "bg". 
         ?ns rdfs:label ?nsLabel .
         ?sex rdfs:label ?sexLabel .
         ?pg rdfs:label ?pgLabel .
         ?mir rdfs:label ?mirLabel .
  }
   bind(if(sameterm(?sex,wd:Q6581097),1,0) as ?M)
   bind(if(sameterm(?sex,wd:Q6581097),0,1) as ?F)
} group by ?nsLabel ?NUM 
order by desc(?NUM)
```

### By Parliamentary group

```sparql
select 
 ?nsLabel ?NUM ?pgLabel (sum(?M) as ?males) (sum(?F) as ?females) 
{
  {select ?x ?ns ?NUM ?sex ?pg {
    ?ns p:P31 [ps:P31 wd:Q43792361 ; pq:P1545 ?num] 
    bind(strdt(?num,xsd:integer) as ?NUM)    
    filter(?NUM >= 39)     
    ?x p:P39 [ps:P39 wd:Q18924508 ; pq:P2937 ?ns ; pq:P768 ?mir ; pq:P4100 ?pg] ; wdt:P21 ?sex .
    ?mir p:P31/pq:P1545 ?mir_num .
  } group by ?x ?ns ?NUM ?sex ?pg }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "bg". 
         ?ns rdfs:label ?nsLabel .
         ?sex rdfs:label ?sexLabel .
         ?pg rdfs:label ?pgLabel .
         ?mir rdfs:label ?mirLabel .
  }
   bind(if(sameterm(?sex,wd:Q6581097),1,0) as ?M)
   bind(if(sameterm(?sex,wd:Q6581097),0,1) as ?F)
} group by ?nsLabel ?NUM ?pgLabel
order by desc(?NUM)
```

### By MIR

```sparql
select 
 ?nsLabel ?NUM ?mirLabel ?MIR_NUM (sum(?M) as ?males) (sum(?F) as ?females) 
{
  {select ?x ?ns ?NUM ?sex ?mir ?MIR_NUM{
    ?ns p:P31 [ps:P31 wd:Q43792361 ; pq:P1545 ?num] 
    bind(strdt(?num,xsd:integer) as ?NUM)    
    filter(?NUM >= 39)     
    ?x p:P39 [ps:P39 wd:Q18924508 ; pq:P2937 ?ns ; pq:P768 ?mir ; pq:P4100 ?pg] ; wdt:P21 ?sex .
    ?mir p:P31/pq:P1545 ?mir_num .
    bind(strdt(?mir_num,xsd:integer) as ?MIR_NUM)    
  } group by ?x ?ns ?NUM ?sex ?mir ?MIR_NUM }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "bg". 
         ?ns rdfs:label ?nsLabel .
         ?sex rdfs:label ?sexLabel .
         ?pg rdfs:label ?pgLabel .
         ?mir rdfs:label ?mirLabel .
  }
   bind(if(sameterm(?sex,wd:Q6581097),1,0) as ?M)
   bind(if(sameterm(?sex,wd:Q6581097),0,1) as ?F)
} group by ?nsLabel ?NUM ?mirLabel ?MIR_NUM
order by desc(?NUM) ?MIR_NUM
```