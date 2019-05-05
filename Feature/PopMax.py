import os 
cwd = os.getcwd()
import json

pop_dic = {}
with open(os.path.join(cwd, "../data/geo_dict_with_population_lonalt.txt")) as f:
    for line in f:
        line = line.strip().split(" ")
        place = line.pop(0)
        i = 0
        pop_list = []
        while i < len(line):
            if line[i + 2] == "NoRecords":
                i += 3
                continue
            geoid = line[i]
            pop = int(line[i + 1])
            pop_list.append((pop, geoid))
            i += 5
        if not pop_list:
            continue
        max_tuple = max(pop_list)
        if max_tuple[0] == pop_list[-1][0]:
            max_tuple = pop_list[-1]
        pop_dic[place] = max_tuple

print("Dictionary Done!")

with open(os.path.join(cwd, "../data/pop_dic.json"), "w") as fp:
    json.dump(pop_dic, fp)
