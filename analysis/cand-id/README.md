#  Proposal for candidate identification in Bulgarian elections open data 

## Current state

Candidates are currently shared by the Central Elections Committee (CEC) as part of the open data dump, in a file named `cik_candidates_DATE.txt` or `local_candidates_DATE.txt`. 
Depending on the election type, candidates are identified by a combination of: 
* the ballot number of the party,
* the constituency (region or municipality)
* their number in the electoral list.
* The candidate's three names

Example from `local_candidates_04.04.2021.txt`
```buildoutcfg
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;119;Кирил Пецев Пецев;
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;120;Славчо Иванов Попов;
1;01. БЛАГОЕВГРАД;4;БСП за БЪЛГАРИЯ;121;Костадин Красимиров Харисков;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;101;Цончо Томов Ганев;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;102;Цвета Валентинова Рангелова;
1;01. БЛАГОЕВГРАД;5;ВЪЗРАЖДАНЕ;103;Александър Сотиров Стойков;
```

In this example, `Александър Сотиров Стойков` is the 3rd candidate of Party nb. 5's list in Blagoevgrad MIR (01)

## Candidate Homonymy

While this is sufficient to identify _the candidacy_ it is not sufficient to identify _the individual_ for whom we dispose only with their three names. Thus,  currently we do not have any mechanism of identification of individuals between elections or even between candidacies in the same election.

The following SPARQL query lists names, which appear in more than 10 candidacies in elections since 2013:

```spaqrl
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
} order by desc(?date)
```
[Try it](https://elections.ontotext.com/sparql?name=%D0%A2%D1%8A%D1%80%D1%81%D1%8F%20%D0%9A%D0%B0%D0%BD%D0%B4%D0%B8%D0%B4%D0%B0%D1%82%20%D0%BF%D0%BE%20%D0%B8%D0%BC%D0%B5&infer=true&sameAs=true&query=%23%20%D0%A2%D1%8A%D1%80%D1%81%D1%8F%20%D0%9A%D0%B0%D0%BD%D0%B4%D0%B8%D0%B4%D0%B0%D1%82%D0%B8%20%D0%BF%D0%BE%20(%D1%87%D0%B0%D1%81%D1%82%20%D0%BE%D1%82)%20%D0%B8%D0%BC%D0%B5%D1%82%D0%BE%20%0A%0APREFIX%20my%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fentity%2F%3E%0APREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0APREFIX%20myd%3A%20%3Chttps%3A%2F%2Felections.ontotext.com%2Fresource%2Fprop%2Fdirect%2F%3E%0Aselect%20%3Fcandidate_uri%20%3Fcandidate_name%20%3Felection_label%20%3Felection_date%20%3Fcandidate_list_number%20%3Fparty_label%20%3Fparty_number%20where%20%7B%20%0A%09%3Fcandidate_uri%20a%20my%3ACandidate%20%3B%20rdfs%3Alabel%20%3Fcandidate_name%20%3B%20myd%3Acandidacy%20%3Fel%20%3B%20myd%3Arepresents%20%3Fparty%20.%0A%20%20%20%20%3Fparty%20rdfs%3Alabel%20%3Fparty_label%20%3B%20myd%3Anumber%20%3Fparty_number.%20%0A%20%20%20%20optional%7B%3Fel%20rdfs%3Alabel%20%3Felection_label%20%3B%20myd%3Adate%20%3Felection_date%7D%0A%20%20%20%20optional%7B%3Fcandidate_uri%20myd%3Anumber%20%3Fcandidate_list_number%7D%0A%20%20%20%20filter(contains(lcase(%3Fcandidate_name)%2C%22%D0%B8%D0%B2%D0%B0%D0%BD%20%D0%B3%D0%B5%D0%BE%D1%80%D0%B3%D0%B8%D0%B5%D0%B2%20%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%22))%0A%7D%20order%20by%20desc(%3Fdate)&execute)

## Proposed solution

It is clear that three names are not enough to identify the individuals from their candidacies. The obvious solution is to distribute the candidate's EGN identifiers, but this is impossible ad it is against current data privacy regulations.
Fortunately, a very similar problem is faced by the Bulgarian Registry agency, who have already proposed a solution. In the open data provided by the Registry Agency, identifiers are anonymized using a [hash function](https://en.wikipedia.org/wiki/Hash_function) (usually) on the individual's EGN identifier. This way the original is obfuscated while the uniquenss of the identification remains. 


Here is an example from the Registry Agency's open data for 16.02.2021 (available [here](https://data.egov.bg/organisation/datasets/resourceView/bd6ae065-1035-4020-89a1-40095288a4a1)) In this JSON snippet, the person named `Никола Красимиров Тулечки` is identified by the string `1065f008ebe9874127eaa2858247d448ebc280f6f6f3da8e5b62458056dbac7c`. This string is guaranteed to be te same for every other mention of the same person in the data.

```json
{ "Person": [
    {
        "$": {
            "CountryCode": "BGR",
            "Position": "Председател на Управителния съвет",
            "IsForeignTraderText": "0"
        },
        "_": "",
        "Indent": [
            {
                "_": "1065f008ebe9874127eaa2858247d448ebc280f6f6f3da8e5b62458056dbac7c"
            }
        ],
        "Name": [
            {
                "_": "Никола Красимиров Тулечки"
            }
        ],
        "IndentType": [
            {
                "_": "EGN"
            }
        ]
    }
  ]
}
```

**We propose to implement the same solution for the election data and alonside the name provide the product of a hash function over the candidate's identifier.** 

## Dataset interoperability

Beside proper identification and deduplication oif the candidate data, a very worthwhile stretch goal would be to ensure **data interoperability between the two datasests**. 

This is relatively straightforward and requires implementing **exactly the same hash function** as the one used by the Trade Registry. 

If this is achieved, it would be guaranteed that if Mr. Tulechki is ever a candidate in an election in Bulgaria, he would receive the same identifier as the one in the trade registry dataset. Such a correspondence will eliminate any ambiguity between the two datasets and pave the way for much more precise data analytics in the future.     
