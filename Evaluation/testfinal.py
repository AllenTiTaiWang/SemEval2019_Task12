import os
cwd = os.getcwd()
import glob
import pandas as pd


pred = pd.read_csv(os.path.join(cwd, "../Model/GEO_pred_test.csv"), na_filter = False)

new = pred["Location"].str.split("/", expand = True)

pred["location"] = new[0]
pred["document"] = new[10].str.split(".", expand = True)[0]

all_files = glob.glob(os.path.join(cwd, "../Feature/Final_dataset/Final_test/*.ann"))
count_all = 0
count_broken = 0
count_thailand = 0
for f in all_files:
    file_name = f.split("/")[7]
    #ann_loc = []
    with open(f, "r") as infile:
        with open(os.path.join(cwd, "testann/" + file_name), "w") as outfile:
            for line in infile:
                line_list = line.strip().split("\t")
                if "T" not in line_list[0] and "#" not in line_list[0]:
                    print("===== Weird Format of Name =====")
                    print("File: " + f)
                    print(line)
                    outfile.write(line)
                    continue
                if "Location" in line_list[1]:
                    outfile.write(line)
                    token = line_list[0].replace("T", "#")
                    location = line_list[2].replace(" ", "_").lower()
                    location = location.replace("-", "")
                    document = file_name.split(".")[0]
                    description = "AnnotatorNotes " + line_list[0]
                    geoloc = pred.loc[(pred["location"] == location) & (pred["document"] == document) & (pred["prediction"] == 1)]
                    if geoloc.empty:
                        location = location.replace("_", "")
                        geoloc = pred.loc[(pred["location"] == location) & (pred["document"] == document) & (pred["prediction"] == 1)]
                    if geoloc.empty:
                        annotation = "<latlng>NA</latlng><geoID>NA</geoID><pop>NA</pop>"
                    else:
                        geoid = geoloc.iloc[0, 1]
                        lat = geoloc.iloc[0, 5]
                        lon = geoloc.iloc[0, 6]
                        pop = geoloc.iloc[0, 4]
                        annotation = "<latlng>" + str(round(lat, 5)) + ", " + str(round(lon, 5)) + "</latlng><pop>" + str(pop) + "</pop><geoID>" + str(geoid) + "</geoID>"   
                    new_line = [token, description, annotation]
                    line_ann = "\t".join(new_line)
                    outfile.write(line_ann + "\n")

