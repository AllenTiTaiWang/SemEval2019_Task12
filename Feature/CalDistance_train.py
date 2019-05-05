import os
cwd = os.getcwd()
import math
from timeit import default_timer as timer
import json
import numpy as np

with open(os.path.join(cwd, '../data/all_doc_train.json'), 'r') as fp:
    all_doc = json.load(fp)

#GEOname = ["madagascar", "asia", "china", "south_korea", "africa"]

#read json to dict
with open(os.path.join(cwd, '../data/geoid2la.json'), 'r') as fp:
    geoid2la = json.load(fp)

with open(os.path.join(cwd, '../data/geoname2id.json'), 'r') as fp:
    geoname2id = json.load(fp)

print("dictionary Done!")

#for k, v in all_doc.items():
#    all_doc[k] = {c : a for c, a in v.items() if c in geoname2id}


all_doc = {k:v for k, v in all_doc.items() if v}


#function of distance
from geopy import distance
def euc_distance(x1, y1, x2, y2):
    cor1 = (x1, y1)
    cor2 = (x2, y2)
    dis = round(distance.distance(cor1, cor2).miles, 3)
    return dis

# GEOname = [minimum_D, geoID_md, minAVG_D, geoID_avgD, MostPOP, geoID_pop]
doc2country = {}
countrynotdic = set()
misscountrycount = {}
doc_country = {}
#The target country
for doc, GEOname in all_doc.items():
    name2dist = {}
    for country, restGEO in GEOname.items():
        flag = False
        id_list = []
        #all of ID from the target
        if not restGEO:
            for geoid_count in geoname2id[country]:
                id_list.append((geoid_count, np.nan, np.nan, geoid2la[geoid_count][2], geoid2la[geoid_count][0], geoid2la[geoid_count][1]))
            name2dist[country] = id_list
            print("country with no neighbors: ", country, geoid_count)
            continue
        if country not in geoname2id:
            country_org = country
            if country.replace("_", "") in geoname2id:
                country = country.replace("_", "") 
            elif country.replace(".", "._") in geoname2id:
                country = country.replace(".", "._")
            elif country.replace("east", "eastern") in geoname2id:
                country = country.replace("east", "eastern")
            elif country.replace("west", "western") in geoname2id:
                country = country.replace("west", "western")
            elif country.replace("south", "southern") in geoname2id:
                country = country.replace("south", "southern")
            elif country.replace("north", "northern") in geoname2id:
                country = country.replace("north", "northern")
            else:
                flag = False
                countrynotdic.add(country)
                if country not in misscountrycount:
                    misscountrycount[country] = 1
                else:
                    misscountrycount[country] += 1
                if doc not in doc_country:
                    doc_country[doc] = [country]
                elif country not in doc_country[doc]:
                    doc_country[doc].append(country)
                continue
            flag = True
        for geoid_count in geoname2id[country]:
            #gey lon, lat, and pop
            lon_count = float(geoid2la[geoid_count][1])
            lat_count = float(geoid2la[geoid_count][0])
            pop_count = float(geoid2la[geoid_count][2])
            total = 0
            min_coun = []
            #The rest of location
            for rest in restGEO:
                if rest not in geoname2id:
                    rest_org = rest
                    if rest.replace("_", "") in geoname2id:
                        rest = rest.replace("_", "") 
                    elif rest.replace(".", "._") in geoname2id:
                        rest = rest.replace(".", "._")
                    elif rest.replace("east", "eastern") in geoname2id:
                        rest = rest.replace("east", "eastern")
                    elif rest.replace("west", "western") in geoname2id:
                        rest = rest.replace("west", "western")
                    elif rest.replace("south", "southern") in geoname2id:
                        rest = rest.replace("south", "southern")
                    elif rest.replace("north", "northern") in geoname2id:
                        rest = rest.replace("north", "northern")
                if rest in geoname2id:
                    dis_all = []
                    #all of ID from the rest
                    for item in geoname2id[rest]:
                        lon = float(geoid2la[item][1])
                        lat = float(geoid2la[item][0])
                        ed = euc_distance(lat_count, lon_count, lat, lon)
                        dis_all.append(ed)
                    total += min(dis_all)
                    min_coun.append(min(dis_all))
                else:
                    countrynotdic.add(rest)
                    if rest not in misscountrycount:
                        misscountrycount[rest] = 1
                    else:
                        misscountrycount[rest] += 1                   
                    if doc not in doc_country:
                        doc_country[doc] = [rest]
                    elif rest not in doc_country[doc]:
                        doc_country[doc].append(rest)
            avg = round((total / len(restGEO)), 2)
            if not min_coun:
                flag = False
                id_list.append((geoid_count, 0, 0, pop_count, lat_count, lon_count))
                continue
            minc = round(min(min_coun), 2)
            id_list.append((geoid_count, minc, avg, pop_count, lat_count, lon_count))
        if flag:
            #print(country)
            country = country_org
            flag = False
        name2dist[country] = list(set(id_list))
    doc2country[doc] = name2dist
doc2country_train = doc2country
print("Calculation Done!")
print("Country not in Dictionary: \n", misscountrycount)
print("Total of involving missing times: ", sum(misscountrycount.values()))
print("length of all missing country: ", len(countrynotdic))
print("==========")
for doc, miss in doc_country.items():
    print("Document: ", doc, " and Location: ", miss)
with open(os.path.join(cwd, '../data/doc2country_train.json'), 'w') as fp:
    doc2country_train = json.dump(doc2country_train, fp)

print("json Done!")
#多包一個字典是Document
