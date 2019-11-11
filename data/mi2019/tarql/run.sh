tarql -d ";" -H cik_parties.tarql  ../tur1/ko/cik_parties_27.10.2019.txt > ../rdf/cik_parties.ttl

tarql -d ";" -H local_parties.tarql  ../tur1/ko/local_parties_27.10.2019.txt > ../rdf/local_parties.ttl

tarql -d ";" -H local_parties.tarql  ../tur1/os/local_parties_27.10.2019.txt >> ../rdf/local_parties.ttl

tarql -d ";" -H  sections_tur1.tarql  ../tur1/ko/sections_27.10.2019.txt > ../rdf/sections_elections_tur1.ttl

tarql -d ";" -H  sections_tur2.tarql  ../tur2/ko/sections_03.11.2019.txt > ../rdf/sections_elections_tur2.ttl

tarql -d ";" -H  candidates_ko_tur1.tarql  ../tur1/ko/local_candidates_27.10.2019.txt > ../rdf/candidates_ko_tur1.ttl

tarql -d ";" -H  candidates_ko_tur2.tarql  ../tur2/ko/local_candidates_03.11.2019.txt > ../rdf/candidates_ko_tur2.ttl

tarql -d ";" -H  candidates_os.tarql  ../tur1/os/local_candidates_27.10.2019.txt > ../rdf/candidates_os.ttl

python flatten.py ../tur1/ko/votes_27.10.2019.txt | tarql --stdin -d ";" -H  vote_ko_tur1.tarql > ../rdf/vote_ko_tur1.ttl

python flatten.py ../tur2/ko/votes_03.11.2019.txt | tarql --stdin -d ";" -H  vote_ko_tur2.tarql > ../rdf/vote_ko_tur2.ttl

python flatten.py ../tur1/os/votes_27.10.2019.txt | tarql --stdin -d ";" -H  vote_os.tarql > ../rdf/vote_os.ttl

#tarql -d ";" -H  preference_os.tarql  ../tur1/os/preferences_27.10.2019.txt > ../rdf/preference_os.ttl

curl "https://docs.google.com/spreadsheets/d/1tPGAecSA5P7Hv5ayYO6IYYkgqTW8gfkWTVn48t15Zj4/gviz/tq?tqx=out:csv&sheet=COALITIONS"  | tarql --stdin coalitions.tarql > ../rdf/coalitions.ttl
curl "https://docs.google.com/spreadsheets/d/1tPGAecSA5P7Hv5ayYO6IYYkgqTW8gfkWTVn48t15Zj4/gviz/tq?tqx=out:csv&sheet=INDEPENDANT" | tarql --stdin independant.tarql > ../rdf/independant.ttl

tarql -d ";" -H  protocols_ko_tur1.tarql  ../tur1/ko/protocols_27.10.2019.txt > ../rdf/protocols_ko_tur1.ttl

tarql -d ";" -H  protocols_os.tarql  ../tur1/os/protocols_27.10.2019.txt > ../rdf/protocols_os.ttl

tarql -d ";" -H  protocols_ko_tur2.tarql  ../tur2/ko/protocols_03.11.2019.txt > ../rdf/protocols_ko_tur2.ttl
