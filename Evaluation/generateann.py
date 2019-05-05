import os
cwd = os.getcwd()
import glob
import pandas as pd


pred = pd.read_csv(os.path.join(cwd, "../Model/GEO_pred_dev.csv"), na_filter = False)

new = pred["Location"].str.split("/", expand = True)

pred["location"] = new[0]
pred["document"] = new[10].str.split(".", expand = True)[0]

all_files = glob.glob(os.path.join(cwd, "../Feature/Final_dataset/actual_dev/*.ann"))
count_all = 0
count_broken = 0
count_thailand = 0
for f in all_files:
    file_name = f.split("/")[7]
    ann_loc = []
    with open(f, "r") as infile:
        with open(os.path.join(cwd, "disambiguation/res/" + file_name), "w") as outfile:
            for line in infile:
                line_list = line.strip().split("\t")
                #print(line_list[1].split(" "))
                if "#" not in line_list[0] and "T" not in line_list[0]:
                    print("===== Weird Format of Name =====")
                    print("File: " + f)
                    outfile.write(line)
                    continue
                if line_list[1].split(" ")[1] in ann_loc:
                    if geoloc.empty:
                        #print("===== Can't Recognize =====")
                        #print("Location Name: " + location)
                        #print("Document: " + document)
                        count_all += 1
                        if "-" in location:
                            count_broken += 1
                        if location == "mueang" or location == "mueng" or location == "sho":
                            count_thailand += 1
                        annotation = "<latlng>NA</latlng><geoID>NA</geoID><pop>NA</pop>"
                        line_list[2] = annotation
                        line_ann = "\t".join(line_list)
                    else:
                        geoid = geoloc.iloc[0, 1]
                        lat = geoloc.iloc[0, 5]
                        lon = geoloc.iloc[0, 6]
                        pop = geoloc.iloc[0, 4]
                        annotation = "<latlng>" + str(round(lat, 5)) + ", " + str(round(lon, 5)) + "</latlng><pop>" + str(pop) + "</pop><geoID>" + str(geoid) + "</geoID>"
                        line_list[2] = annotation
                        line_ann = "\t".join(line_list)
                    ann_loc.remove(line_list[1].split(" ")[1])
                    outfile.write(line_ann + "\n")
                    continue

                elif "Location" in line_list[1]:
                    token = line_list[0]
                    ann_loc.append(token)
                    location = line_list[2].replace(" ", "_").lower()
                    location = location.replace("-", "")
                    document = file_name.split(".")[0]
                    geoloc = pred.loc[(pred["location"] == location) & (pred["document"] == document) & (pred["prediction"] == 1)]
                    if geoloc.empty:
                        location = location.replace("_", "")
                        geoloc = pred.loc[(pred["location"] == location) & (pred["document"] == document) & (pred["prediction"] == 1)]
                    outfile.write(line)


