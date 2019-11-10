tarql -d ";" -H  sections_tur1.tarql  ../tur1/ko/sections_27.10.2019.txt > ../rdf/sections_elections_tur1.ttl

tarql -d ";" -H  sections_tur2.tarql  ../tur2/ko/sections_03.11.2019.txt > ../rdf/sections_elections_tur2.ttl

tarql -d ";" -H  candidates_ko_tur1.tarql  ../tur1/ko/local_candidates_27.10.2019.txt > ../rdf/candidates_ko_tur1.ttl

tarql -d ";" -H  candidates_ko_tur2.tarql  ../tur2/ko/local_candidates_03.11.2019.txt > ../rdf/candidates_ko_tur2.ttl

tarql -d ";" -H  candidates_os.tarql  ../tur1/os/local_candidates_27.10.2019.txt > ../rdf/candidates_os.ttl

python flatten.py ../tur1/ko/votes_27.10.2019.txt | tarql --stdin -d ";" -H  vote_ko_tur1.tarql > ../rdf/vote_ko_tur1.ttl

python flatten.py ../tur2/ko/votes_03.11.2019.txt | tarql --stdin -d ";" -H  vote_ko_tur2.tarql > ../rdf/vote_ko_tur2.ttl

python flatten.py ../tur1/os/votes_27.10.2019.txt | tarql --stdin -d ";" -H  vote_os.tarql > ../rdf/vote_os.ttl

#tarql -d ";" -H  preference_os.tarql  ../tur1/os/preferences_27.10.2019.txt > ../rdf/preference_os.ttl