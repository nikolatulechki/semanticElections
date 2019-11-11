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


## Местни Коалиции 



## Protocols

.
####
?b ?SEC_ID  Пълен код на секция

?e myd:recieved_ballots  5) A.   Брой на бюлетините, получени по реда на чл. 215, ал. 1 ИК, вписани в 
?f myd:voters_count  6) 1.   Брой на избирателите според избирателния списък при предаването му на  СИК (сумата от числата по букви „а“ и „б“ от тази точка)
  7) 1.а) Избирателен списък – част І
  8) 1.б) Избирателен списък – част ІІ
?i myd:voters_additional_count  9) 2.   Брой на избирателите, вписани в допълнителната страница (под чертата)  на избирателния списък в изборния ден
?j myd:voters_voted_count 10) 3.   Брой на гласувалите избиратели според положените подписи в избирателния
 11) 4.а) брой на неизползваните бюлетини
 12) 4.б) брой на унищожените от СИК бюлетини по други поводи (за създаване на образци за таблата пред изборното помещение и увредени механично при           откъсване от кочана)
 13) 4.в) брой на недействителните бюлетини по чл. 427, ал. 6 ИК (когато номерът
          на бюлетината не съответства на номер в кочана)
 14) 4.г) брой на недействителните бюлетини по чл. 227 ИК
          (при които е използвана възпроизвеждаща техника)
 15) 4.д) брой на недействителните бюлетини по чл. 228 ИК
          (показан публично вот след гласуване)
 16) 4.е) брой на сгрешените бюлетини по чл. 267, ал. 2 ИК
 17) 5.   Брой на намерените в избирателната кутия бюлетини
?r myd:votes_invalid_count 
18) 6.   Брой намерени в избирателната кутия недействителни гласове (бюлетини)
 19) 7.   Общ брой на намерените в избирателната кутия действителни гласове
          (бюлетини) (сумата от числата по т. 7.1 и т. 7.2)
?t myd:votes_valid_count 20) 7.1. Брой на действителните гласове, подадени за кандидатските листи на партии, коалиции и инициативни комитети
?u myd:votes_blanc_count 21) 7.2. Брой на действителните гласове с отбелязан вот в квадратчето
          „Не подкрепям никого“
?v myd:ballots_empty 22) 9.   Празни бюлетини или бюлетини, в които е гласувано за повече от
          една листа, както и бюлетини, в които не може да се установи
          еднозначно вотът на избирателя
