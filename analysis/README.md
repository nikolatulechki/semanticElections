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

