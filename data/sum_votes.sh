cat ../gdrive/data/cikOpenData/pi2021_07/votes_11.07.2021.flat.txt | csvtk summary -H -d ";" -w 0 -i -g 1,2 -f 3:sum > ../gdrive/data/cikOpenData/pi2021_07/votes_11.07.2021.flat.sum.txt
cat ../gdrive/data/cikOpenData/pi2021_11/votes_14.11.2021.flat.txt | csvtk summary -H -d ";" -w 0 -i -g 1,2 -f 3:sum > ../gdrive/data/cikOpenData/pi2021_11/votes_14.11.2021.flat.sum.txt
cat ../gdrive/data/cikOpenData/pi2022/votes_02.10.2022.flat.txt | csvtk summary -H -d ";" -w 0 -i -g 1,2 -f 3:sum > ../gdrive/data/cikOpenData/pi2022/votes_02.10.2022.flat.sum.txt

cat ../gdrive/data/cikOpenData/pi2022/preferences_02.10.2022.txt | grep -v -E -e "(Без|;0)\b" | csvtk summary -H -d ";" -w 0 -i -g 1,2,3,4 -f 5:sum >  ../gdrive/data/cikOpenData/pi2022/preferences_02.10.2022.sum.txt
cat ../gdrive/data/cikOpenData/pi2021_11/preferences_14.11.2021.txt | grep -v -E -e "(Без|;0)\b" | csvtk summary -H -d ";" -w 0 -i -g 1,2,3,4 -f 5:sum >  ../gdrive/data/cikOpenData/pi2021_11/preferences_14.11.2021.sum.txt
cat ../gdrive/data/cikOpenData/pi2021_07/preferences_11.07.2021.txt | grep -v -E -e "(Без|;0)\b" | csvtk summary -H -d ";" -w 0 -i -g 1,2,3,4 -f 5:sum >  ../gdrive/data/cikOpenData/pi2021_07/preferences_11.07.2021.sum.txt
