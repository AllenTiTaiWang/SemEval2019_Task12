import os
cwd = os.getcwd()
from operator import itemgetter
import json

with open(os.path.join(cwd, '../data/doc2country_test.json'), "r") as fp:
    doc2country = json.load(fp)

print("Load Done!")

total = 0
count_min = 0
count_avg = 0
for doc, countries in doc2country.items():
    with open(os.path.join(cwd, '../data/test/%s.txt' % doc), 'w') as f:
        for country, value in countries.items():
            #min_min = min(value, key = itemgetter(1))
            #avg_min = min(value, key = itemgetter(2))
            for item in value:
                geo_id = item[0]
                minc = item[1]
                avg = item[2]
                #pop = pop_dic[country]
                pop = item[3]
                lat = item[4]
                lon = item[5]
                #if str(minc) == str(pop_max[1]):
                    #count_min += 1
                #if str(avg) == str(pop_max[1]):
                    #count_avg += 1
                #total += 1
                line_w = str(country) + " " + str(geo_id) + " " + str(minc) + " " + str(avg) + " " + str(pop) + " " + str(lat) + " " + str(lon) + "\n"
                f.write(line_w)
    f.close()

#print("Accuracy of minimum: ", count_min / total)
#print("Accuracy of average: ", count_avg / total)
