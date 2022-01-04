import pandas as pd
import numpy as np
from os import listdir

DAMAN = "../../jalend/ParsedData/Daman/"
MANIPUR = "../../jalend/ParsedData/Manipur/"
MEGHALAYA = "../../jalend/ParsedData/Meghalaya/"
NAGALAND = "../../jalend/ParsedData/Nagaland/"
ARUNACHAL = "../../jalend/ParsedData/ArunachalPradesh/"
DELHI = "../DataSets/ElectoralRollsData/ParsedData/Delhi/"
SIKKIM = "../DataSets/ElectoralRollsData/ParsedData/Sikkim/"
GOA = "../DataSets/ElectoralRollsData/ParsedData/GoaParsed/"
MIZORAM = "../DataSets/ElectoralRollsData/ParsedData/Mizoram/"

DAMAN_CSV = "../DataSets/ElectoralRollsData/MergedCSV/daman.csv"
MANIPUR_CSV = "../DataSets/ElectoralRollsData/MergedCSV/manipur.csv"
MEGHALAYA_CSV = "../DataSets/ElectoralRollsData/MergedCSV/meghalaya.csv"
NAGALAND_CSV = "../DataSets/ElectoralRollsData/MergedCSV/nagaland.csv"
ARUNACHAL_CSV = "../DataSets/ElectoralRollsData/MergedCSV/arunachal.csv"
DELHI_CSV = "../DataSets/ElectoralRollsData/MergedCSV/delhi.csv"
SIKKIM_CSV = "../DataSets/ElectoralRollsData/MergedCSV/sikkim.csv"
GOA_CSV = "../DataSets/ElectoralRollsData/MergedCSV/goa.csv"
MIZORAM_CSV = "../DataSets/ElectoralRollsData/MergedCSV/mizoram.csv"
CBSE_NO_DUP = "../DataSets/CBSEData/cbse_gender_names_list.csv"
CBSE = "../DataSets/CBSEData/cbse_data_with_duplicates.csv"

def getCBSEData(dup):
    if dup:
        cbse_df = pd.read_csv(CBSE)
    else:
        cbse_df = pd.read_csv(CBSE_NO_DUP)
    del cbse_df['Unnamed: 0']
    return cbse_df

def getStateData(files, loc):
    req = []
    for file in files:
        if ".csv" in file:
            req.append(file)
    df = pd.concat([pd.read_csv(loc+file, header=0, names=['name','father_name','husband_name','mother_name','house_number','gender','age']) for file in req], ignore_index=True)
    return df

def cleanDf(df, col):
    df = df.drop_duplicates()
    df['Name'] = df['Name'].str.lower()
    df['len']= [len(str(i)) for i in df[col]]
    # Name cannot be of just 2 characters
    df = df[df['len'] >= 2]
    print(df.groupby('Gender')['Name'].count()) #stats
    return df

def getERData(loc):
    daman = pd.read_csv(loc+DAMAN_CSV)
    manipur = pd.read_csv(loc+MANIPUR_CSV)
    meghalaya = pd.read_csv(loc+MEGHALAYA_CSV)
    nagaland = pd.read_csv(loc+NAGALAND_CSV)
    arunachal =pd.read_csv(loc+ARUNACHAL_CSV)
    delhi = pd.read_csv(loc+DELHI_CSV)
    sikkim = pd.read_csv(loc+SIKKIM_CSV)
    goa = getStateData(listdir(loc+GOA), loc+GOA)
    mizoram = pd.read_csv(loc+MIZORAM_CSV)
    er = pd.concat([daman, manipur, meghalaya, nagaland, arunachal, delhi, sikkim, goa, mizoram], ignore_index = True)
    er = er.rename(columns={'name':'Name', 'gender':'Gender'})
    return er
    

