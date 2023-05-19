from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import wkt
import csv, re

with open("converted/mi2019.csv") as file:
    next(csv.reader(file))
    temp = {}
    for row in csv.reader(file):
        m = re.search("\((..)\)",row[2])
        if m:
            reg = m.group(1)
            sec = row[3].zfill(3)
            regsec = reg+sec
            if regsec in temp.keys():
               temp[regsec].append(wkt.loads(row[0]))
            else:
               temp[regsec]=[wkt.loads(row[0])]

for regsec in temp.keys():
    joined = unary_union(temp[regsec])
    print(regsec+";"+joined.wkt)



