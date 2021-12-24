#  Proposal for candidate identification in Bulgarian elections open data 

## Current state

Candidates are currently shared by the Central Elections Committee (CEC) as part of the open data dump, in a file named `cik_candidates_DATE.txt` or `local_candidates_DATE.txt`. 
Depending on the election type, candidates are identified by a combination of: 
* the ballot number of the party,
* the constituency (region or municipality)
* their number in the electoral list.
* The candidate's three names

Example from `local_candidates_04.04.2021.txt`
```csv
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;119;Кирил Пецев Пецев;
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;120;Славчо Иванов Попов;
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;121;Костадин Красимиров Харисков;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;101;Цончо Томов Ганев;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;102;Цвета Валентинова Рангелова;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;103;Александър Сотиров Стойков;
```

In this example, `Александър Сотиров Стойков` is the 3rd candidate of Party nb. 5's list in Blagoevgrad MIR (01)

## Candidate Homonymy

While this is sufficient to identify _the candidacy_ it is not sufficient to identify _the individual_. This is because across elections, we can rely only on their three names. Thus, currently **we do not have any mechanism of identification of individuals between elections** or even between candidacies in the same election.

Let's illustrate this! The following SPARQL query lists names, which appear in more than 10 candidacies in elections since 2013:

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select ?norm_name (count(*) as ?count) where { 
	?candidate_uri a my:Candidate ; rdfs:label ?candidate_name .
    bind(lcase(?candidate_name) as ?norm_name)
} group by ?norm_name having(?count > 10) order by desc(?count)
```
[Try it](https://elections.ontotext.com/sparql?name=&infer=true&sameAs=true&query=PREFIX%20my%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fentity%2F%3E%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20myd%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fprop%2Fdirect%2F%3E%0Aselect%20%3Fnorm_name%20(count(*)%20as%20%3Fcount)%20where%20%7B%20%0A%09%3Fcandidate_uri%20a%20my%3ACandidate%20%3B%20rdfs%3Alabel%20%3Fcandidate_name%20.%0A%20%20%20%20bind(lcase(%3Fcandidate_name)%20as%20%3Fnorm_name)%0A%7D%20group%20by%20%3Fnorm_name%20having(%3Fcount%20%3E%2010)%20order%20by%20desc(%3Fcount)&execute) 

We can see that very common name combinations such as "георги иванов георгиев" or "петър георгиев петров" appear many tens of times in the data.

Analysis of one of the most frequent candidate names shows how difficult it is to decide how many people this set of candidacies concerns and why a stable and unambiguous  means of identification is necessary. 

```sparql
PREFIX my: <https://elections.ontotext.com/resource/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myd: <https://elections.ontotext.com/resource/prop/direct/>
select ?candidate_uri ?candidate_name ?election_label ?election_date ?candidate_list_number ?party_label ?party_number where { 
	?candidate_uri a my:Candidate ; rdfs:label ?candidate_name ; myd:candidacy ?el ; myd:represents ?party .
    ?party rdfs:label ?party_label ; myd:number ?party_number. 
    optional{?el rdfs:label ?election_label ; myd:date ?election_date}
    optional{?candidate_uri myd:number ?candidate_list_number}
    filter(contains(lcase(?candidate_name),"иван георгиев иванов"))
} order by desc(?election_date)
```
[Try it](https://elections.ontotext.com/sparql?name=%D0%A2%D1%8A%D1%80%D1%81%D1%8F%20%D0%9A%D0%B0%D0%BD%D0%B4%D0%B8%D0%B4%D0%B0%D1%82%20%D0%BF%D0%BE%20%D0%B8%D0%BC%D0%B5&infer=true&sameAs=true&query=%23%20%D0%A2%D1%8A%D1%80%D1%81%D1%8F%20%D0%9A%D0%B0%D0%BD%D0%B4%D0%B8%D0%B4%D0%B0%D1%82%D0%B8%20%D0%BF%D0%BE%20(%D1%87%D0%B0%D1%81%D1%82%20%D0%BE%D1%82)%20%D0%B8%D0%BC%D0%B5%D1%82%D0%BE%20%0A%0APREFIX%20my%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fentity%2F%3E%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20myd%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fprop%2Fdirect%2F%3E%0Aselect%20%3Fcandidate_uri%20%3Fcandidate_name%20%3Felection_label%20%3Felection_date%20%3Fcandidate_list_number%20%3Fparty_label%20%3Fparty_number%20where%20%7B%20%0A%09%3Fcandidate_uri%20a%20my%3ACandidate%20%3B%20rdfs%3Alabel%20%3Fcandidate_name%20%3B%20myd%3Acandidacy%20%3Fel%20%3B%20myd%3Arepresents%20%3Fparty%20.%0A%20%20%20%20%3Fparty%20rdfs%3Alabel%20%3Fparty_label%20%3B%20myd%3Anumber%20%3Fparty_number.%20%0A%20%20%20%20optional%7B%3Fel%20rdfs%3Alabel%20%3Felection_label%20%3B%20myd%3Adate%20%3Felection_date%7D%0A%20%20%20%20optional%7B%3Fcandidate_uri%20myd%3Anumber%20%3Fcandidate_list_number%7D%0A%20%20%20%20filter(contains(lcase(%3Fcandidate_name)%2C%22%D0%B8%D0%B2%D0%B0%D0%BD%20%D0%B3%D0%B5%D0%BE%D1%80%D0%B3%D0%B8%D0%B5%D0%B2%20%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%22))%0A%7D%20order%20by%20desc(%3Felection_date)&execute)

## Proposed solution

It is clear that three names are not enough to identify the individuals from their candidacies. The obvious solution is to distribute the candidate's EGN identifiers, but this is impossible ad it is against current data privacy regulations. 
Our proposition is in accordance with the anonymisation procedure in [Article 15,4](https://www.lex.bg/en/laws/ldoc/2136995819#i_19) of "НАРЕДБА ЗА ОБЩИТЕ ИЗИСКВАНИЯ КЪМ ИНФОРМАЦИОННИТЕ СИСТЕМИ, РЕГИСТРИТЕ И ЕЛЕКТРОННИТЕ АДМИНИСТРАТИВНИ УСЛУГИ" and has the following features:

* It generates a unique identifier based on an individual's three names and part of the EGN number
* It does not require the full EGN number in the input, thus assuring identification without any danger of potentially revealing the EGN number
* It is not reversible and not susceptible to brute-forcing attacks as hashing just the EGN would be
* Does not require sharing secrets as the current solution in the Trade Registry and is thus adapted for widespread adoption for bettering data interoperability

In order to generate a stable identifier for an individual without revealing his EGN number we apply SHA256 to a concatenation of the lowercase variants of the individual's first middle and last name and the first 7 digits of their EGN number. for "Никола Красимиров Тулечки",  EGN 8404236***, 

```SHA256("николакрасимировтулечки8404236") = 00bd86e8887e95525fb08db52c938dbc3f60f537f4df5c65f56d33acb2861b94```    

In order to control for consistency and avoid unwanted variants we propose adding the following constraints.
* only lowercase cyrillic letters from the bulgarian alphabet are allowed
* any spaces are removed (this is done to avoid ambiguity due to the plethora of spacing characters out there)

The input string of the hash function should match the following regex
`/^абвгдежзийклмнопрстуфхцчшщъьюя+[0-9]{7}$/`

# Same list homonym examples 

The following 3 occurences come from 2019 municipal elections and represent cases where the same 3 nаmes appear in the same candidates list.

Георги Василев Георгиев - Община Аксаково - ДПС

* [OIK Link](https://oik0302.cik.bg/mi2019/registers/candidates?t=2)
* [109](https://elections.ontotext.com/resource/candidate/mi2019/os/0302/55/109), [118](https://elections.ontotext.com/resource/candidate/mi2019/os/0302/55/118)

Милко Йорданов Димитров - Община Велики Преслав - ГЕРБ 

* [OIK link](https://oik2723.cik.bg/mi2019/registers/candidates?t=2)
* [104](https://elections.ontotext.com/resource/candidate/mi2019/os/2723/43/115), [115](https://elections.ontotext.com/resource/candidate/mi2019/os/2723/43/104)

Иван Димитров Иванов - Община Ямбол - АТАКА 

* [OIK link](https://oik2826.cik.bg/mi2019/registers/candidates?t=2)
* [111](https://elections.ontotext.com/resource/candidate/mi2019/os/2826/4/111), [115](https://elections.ontotext.com/resource/candidate/mi2019/os/2826/4/115) 





