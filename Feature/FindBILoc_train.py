import os
cwd = os.getcwd()
import json
import glob


# extract location 
all_doc = {}
for filename in glob.glob(os.path.join(cwd, "Final_dataset/actual_train/*.ann")):
    with open(filename, "r") as infile:
        filename = filename.split("/")[8].split(".")[0]
        all_doc[filename] = []
        for line in infile:
            line = line.strip().split("\t")
            if "#" not in line[0] and "T" not in line[0]:
                if " " in line[0]:
                   line[0] = line[0].replace(" ", "")
                bloc = all_doc[filename].pop()
                align = [bloc, line[0].lower()]
                location = "".join(align)
                all_doc[filename].append(location)
                continue
            if "Location" in line[1]:
                line[2] = line[2].replace("-", "")
                line[2] = line[2].replace(" ", "_")
                line[2] = line[2].replace(",", "")
                line[2] = line[2].replace(")", "")
                line[2] = line[2].replace("(", "")
                all_doc[filename].append(line[2].lower())

# Kill empty list
all_doc = { k:v for k,v in all_doc.items() if v }
#print("all_doc")
#print(all_doc)
#print("==========")

doc_all = {}

for doc, loc in all_doc.items():
    #all_doc[doc] = list(set(loc))
    doc_all[doc] = {}
    for i in range(len(loc)):
        country = loc[i]
        if len(set(loc)) == 1:
            doc_all[doc][country] = []
            print("No other country in", doc, " with ", loc)
        if i != len(loc) - 1:
            next_loc = loc[i + 1]
            if country != next_loc:
                if country in doc_all[doc]:
                    doc_all[doc][country].append(next_loc)
                else:
                    doc_all[doc][country] = [next_loc]
                if next_loc in doc_all[doc]:
                    doc_all[doc][next_loc].append(country)
                else:
                    doc_all[doc][next_loc] = [country]

#print("doc_all:")
#print(doc_all)
#print("==========")
all_doc_train = doc_all
with open(os.path.join(cwd, "../data/all_doc_train.json"), "w") as fp:
    all_doc_train = json.dump(all_doc_train, fp)
