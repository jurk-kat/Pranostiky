#Cleaning meteo data. Nicer version with comments in the jupiter notebook

import pandas as pd

def open_file(file_path):
    stanice = []
    with open(file_path, mode="r", encoding="utf-8") as my_file:
        for line in my_file:
            line = line.split(",")
            line = [item.replace("°", "") for item in line]
            line = [item.replace("\n", "") for item in line]
            stanice.append(line)
    return stanice

def meteo_souradnice(stanice):
    souradnice = []
    for line in stanice:
        souradnice.append([line[2], line[4]])
    return souradnice

def seznam_stanic(stanice):
    souradnice = []
    for line in stanice:
        souradnice.append([line[0], line[2], line[4], line[6]])
    return souradnice

file_path = "data/01_stanice.csv"
stanice = open_file(file_path)
stanice = stanice[1:]

souradnice = meteo_souradnice(stanice)
df_souradnice = pd.DataFrame(souradnice, columns = ["latitude", "longitude"])
df_souradnice.to_csv("data/02_souradnice.csv", index=False, encoding="utf-8")

souradnice = seznam_stanic(stanice)
df_souradnice = pd.DataFrame(souradnice, columns = ["location_id", "latitude", "longitude", "elevation"])
df_souradnice.to_csv("data/03_stanice.csv", encoding="utf-8")


