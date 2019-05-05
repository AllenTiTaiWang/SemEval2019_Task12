
import os
cwd = os.getcwd()
import math
from timeit import default_timer as timer
import json

GEOname = ["madagascar", "asia", "china", "south_korea", "africa"]


#Build dictionary for geo
start = timer()
geoname2id = {}
geoid2la = {}
with open(os.path.join(cwd, "../data/geo_dict_with_population_lonalt.txt")) as f:
    for line in f:
        line = line.strip().split(" ")
        place = line.pop(0)
        geoid_l = []
        i = 0
        while i < len(line):
            if line[i + 2] == "NoRecords":
                i += 3
                continue
            geoid = line[i]
            lon = line[i + 2]
            lat = line[i + 3]
            pop = line[i + 1]
            geoid_l.append(geoid)
            geoid2la[geoid] = [lon, lat, pop]
            i += 5
        geoname2id[place] = geoid_l
print("Dictionary Done!")
end = timer()
print(end - start)

#dump to json
with open(os.path.join(cwd, "../data/geoname2id.json"), "w") as fp:
    json.dump(geoname2id, fp)

print("done geoname2id!")

with open(os.path.join(cwd, "../data/geoid2la.json"), "w") as fp2:
    json.dump(geoid2la, fp2)

print("done geoid2la!")

