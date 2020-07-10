tarql -d ";" -H  sections_tur1.tarql  ../tur1/ko/sections_27.10.2019.txt > ../rdf/sections_elections_tur1.ttl

tarql -d ";" -H  sections_tur2.tarql  ../tur2/ko/sections_03.11.2019.txt > ../rdf/sections_elections_tur2.ttl


#tarql -d ";" -H  preference_os.tarql  ../tur1/os/preferences_27.10.2019.txt > ../rdf/preference_os.ttl

curl "https://docs.google.com/spreadsheets/d/1tPGAecSA5P7Hv5ayYO6IYYkgqTW8gfkWTVn48t15Zj4/gviz/tq?tqx=out:csv&sheet=COALITIONS"  | tarql --stdin coalitions.tarql > ../rdf/coalitions.ttl
curl "https://docs.google.com/spreadsheets/d/1tPGAecSA5P7Hv5ayYO6IYYkgqTW8gfkWTVn48t15Zj4/gviz/tq?tqx=out:csv&sheet=INDEPENDANT" | tarql --stdin independant.tarql > ../rdf/independant.ttl

tarql -t sections_geo_wkt.tarql  ../sections_geography.csv > ../rdf/sections_geo.ttl