import os
cwd = os.getcwd()
import pandas as pd
import glob
import numpy as np

column_names = ["Location", "geoID", "min_distance", "avg_distance", "max_population", "lat", "lon"]


all_files = glob.glob(os.path.join(cwd,"../data/train/*.txt"))

con_f = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f, sep = " ", names = column_names, na_filter = False)
    df['Location'] = df['Location'] + '%s' % f
    con_f = con_f.append(df)

con_f['min_distance'] = con_f['min_distance'].astype(float)
con_f['avg_distance'] = con_f['avg_distance'].astype(float)

con_f['min_distance'].fillna((con_f['min_distance'].mean()), inplace=True)
con_f['avg_distance'].fillna((con_f['avg_distance'].mean()), inplace=True)
df = con_f

df["label"] = 0

#id_set = set()
for filename in glob.glob(os.path.join(cwd, "../Feature/Final_dataset/actual_train/*.ann")):
    id_set = set()
    with open(filename, "r") as infile:
        for line in infile:
            line = line.strip().split("\t")
            if len(line) < 3:
                continue
            if "<geoID>" in line[2]:
                geoid = line[2].split("<geoID>")[1].split("</geoID>")[0].strip()
                id_set.add(geoid)
        df.loc[(df["Location"].str.contains(filename.split("/")[10].split(".")[0])) & (df["geoID"].astype('str').isin(id_set)), "label"] = 1
        #print(df["Location"].str.split("/", expand = True)[10])
        #print(df.loc[df["Location"].str.split("/", expand = True)[10].str.contains(filename.split("/")[10].split(".")[0])])
        #print("===")
#df["label"] = df.geoID.map(lambda x: 1 if str(x) in id_set else 0)
#df["frequency"] = df.geoID.map(gold)
#df.update(df["frequency"].fillna(0))
df.to_csv("GEO_train.csv", index = False)


#########################
#########################
#########################

all_files = glob.glob(os.path.join(cwd,"../data/dev/*.txt"))
#df = pd.concat((pd.read_csv(f, sep = " ", names = column_names, na_filter = False) for f in all_files))

con_f = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f, sep = " ", names = column_names, na_filter = False)
    df['Location'] = df['Location'] + '%s' % f
    con_f = con_f.append(df)

con_f['min_distance'] = con_f['min_distance'].astype(float)
con_f['avg_distance'] = con_f['avg_distance'].astype(float)
con_f['min_distance'].fillna((con_f['min_distance'].mean()), inplace=True)
con_f['avg_distance'].fillna((con_f['avg_distance'].mean()), inplace=True)
df = con_f
df["label"] = 0
for filename in glob.glob(os.path.join(cwd, "../Feature/Final_dataset/actual_dev/*.ann")):
    id_set = set()
    with open(filename, "r") as infile:
        for line in infile:
            line = line.strip().split("\t")
            if len(line) < 3:
                continue
            if "<geoID>" in line[2]:
                geoid = line[2].split("<geoID>")[1].split("</geoID>")[0].strip()
                id_set.add(geoid)
        df.loc[(df["Location"].str.contains(filename.split("/")[10].split(".")[0])) & (df["geoID"].astype('str').isin(id_set)), "label"] = 1


df.to_csv("GEO_dev.csv", index = False)
##########################
##########################
##########################
all_files = glob.glob(os.path.join(cwd,"../data/test/*.txt"))

con_f = pd.DataFrame()
for f in all_files:
    df = pd.read_csv(f, sep = " ", names = column_names, na_filter = False)
    df['Location'] = df['Location'] + '%s' % f
    con_f = con_f.append(df)

con_f['min_distance'] = con_f['min_distance'].astype(float)
con_f['avg_distance'] = con_f['avg_distance'].astype(float)

con_f['min_distance'].fillna((con_f['min_distance'].mean()), inplace=True)
con_f['avg_distance'].fillna((con_f['avg_distance'].mean()), inplace=True)
df = con_f

df.to_csv("GEO_test.csv", index = False)


