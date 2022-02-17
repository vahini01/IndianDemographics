import pandas as pd
import numpy as np

DAMAN_CSV = "Models/Data/ERData/daman.csv"
MANIPUR_CSV = "Models/Data/ERData/manipur.csv"
MEGHALAYA_CSV = "Models/Data/ERData/meghalaya.csv"
NAGALAND_CSV = "Models/Data/ERData/nagaland.csv"
ARUNACHAL_CSV = "Models/Data/ERData/arunachal.csv"
DELHI_CSV = "Models/Data/ERData/delhi.csv"
SIKKIM_CSV = "Models/Data/ERData/sikkim.csv"
GOA_CSV = "Models/Data/ERData/goa.csv"
MIZORAM_CSV = "Models/Data/ERData/mizoram.csv"

def processDf(df):
  df['Name'] = [str(name).strip() for name in df['Name']]
  df['Name'] = [name.lower() for name in df['Name']]
  return df

def addFrequency(df):
  df['female_freq'] = df['Name'].map(df[df['Gender']=='FEMALE']['Name'].value_counts())
  df['male_freq'] = df['Name'].map(df[df['Gender']=='MALE']['Name'].value_counts())
  return df

def useMajorityLabel(df):
  df['new_labels'] = 0.0
  labels = []
  for i, name in enumerate(df['Name']):
    if np.isnan(df['female_freq'][i]) or df['male_freq'][i] > df['female_freq'][i]:
      # labels.append(1) 1 for MALE
      df.at[i,'new_labels'] = 1
    else:
      # labels.append(0) 0 for FEMALE
      df.at[i,'new_labels'] = 0
  return df

def dropDuplicates(df):
  df = df.drop_duplicates(subset='Name', keep='last')
  # drop columns where gender is NaN
  df = df[df['Gender'].notna()]
  df = df.reset_index(drop=True)
  return df

def extract_df(loc):
    # Drop duplicates and take majority label
    df = pd.read_csv(loc)
    names_df = pd.DataFrame()
    names_df['Name'] = df['name']
    names_df['Gender'] = df['gender']
    return names_df

def ERState_df(loc):
    names = extract_df(loc)
    names = processDf(names)
    names = addFrequency(names)
    names = useMajorityLabel(names)
    names = dropDuplicates(names)
    #import pdb; pdb.set_trace()
    final_df = pd.DataFrame()
    final_df['Name'] = names['Name']
    final_df['Gender'] = names['new_labels']
    return final_df

def ERState_df_with_dup(loc):
    names = extract_df(loc)
    names = processDf(names)
    return names

def ERData_with_dup():
    daman = ERState_df_with_dup(DAMAN_CSV)
    manipur = ERState_df_with_dup(MANIPUR_CSV)
    meghalaya = ERState_df_with_dup(MEGHALAYA_CSV)
    nagaland = ERState_df_with_dup(NAGALAND_CSV)
    arunachal =ERState_df_with_dup(ARUNACHAL_CSV)
    delhi = ERState_df_with_dup(DELHI_CSV)
    sikkim = ERState_df_with_dup(SIKKIM_CSV)
    goa = ERState_df_with_dup(GOA_CSV)
    mizoram = ERState_df_with_dup(MIZORAM_CSV)
    er = pd.concat([daman, manipur, meghalaya, nagaland, arunachal, delhi, sikkim, goa, mizoram], ignore_index = True)
    return er

def getStateData(files, loc):
    req = []
    for file in files:
        if ".csv" in file:
            req.append(file)
    df = pd.concat([pd.read_csv(loc+file, header=0, names=['name','father_name','husband_name','mother_name','house_number','gender','age'], 
                               dtype = {'name':str,'father_name':str,'husband_name':str,'mother_name':str,'house_number':str,'gender':str,'age':str}) for file in req], ignore_index=True)
    return df
    
def getERData():
    daman = ERState_df(DAMAN_CSV)
    manipur = ERState_df(MANIPUR_CSV)
    meghalaya = ERState_df(MEGHALAYA_CSV)
    nagaland = ERState_df(NAGALAND_CSV)
    arunachal =ERState_df(ARUNACHAL_CSV)
    delhi = ERState_df(DELHI_CSV)
    sikkim = ERState_df(SIKKIM_CSV)
    goa = ERState_df(GOA_CSV)
    mizoram = ERState_df(MIZORAM_CSV)
    er = pd.concat([daman, manipur, meghalaya, nagaland, arunachal, delhi, sikkim, goa, mizoram], ignore_index = True)
#     er = er.rename(columns={'name':'Name', 'gender':'Gender'})
    names = addFrequency(er)
    names = useMajorityLabel(names)
    names = dropDuplicates(names)
#     import pdb; pdb.set_trace()
    final_df = pd.DataFrame()
    final_df['Name'] = names['Name']
    final_df['Gender'] = names['new_labels']
    return er


#  Applying majority over all states 
def ERStateData_with_freq(loc):
    names = extract_df(loc)
    names = processDf(names)
    names = addFrequency(names)
    names = useMajorityLabel(names)
    names = dropDuplicates(names)
    return names

def update_freq(df):
    df['new_male_freq']=df.groupby(['Name'])['male_freq'].transform('sum')
    df['new_female_freq'] = df.groupby(['Name'])['female_freq'].transform('sum')
    df['male_freq'] = df['new_male_freq']
    df['female_freq'] = df['new_female_freq']
    return df

def ERData_MajorityLabel():
    daman = ERStateData_with_freq(DAMAN_CSV)
    manipur = ERStateData_with_freq(MANIPUR_CSV)
    meghalaya = ERStateData_with_freq(MEGHALAYA_CSV)
    nagaland = ERStateData_with_freq(NAGALAND_CSV)
    arunachal =ERStateData_with_freq(ARUNACHAL_CSV)
    delhi = ERStateData_with_freq(DELHI_CSV)
    sikkim = ERStateData_with_freq(SIKKIM_CSV)
    goa = ERStateData_with_freq(GOA_CSV)
    mizoram = ERStateData_with_freq(MIZORAM_CSV)
    er = pd.concat([daman, manipur, meghalaya, nagaland, arunachal, delhi, sikkim, goa, mizoram], ignore_index = True)
    # update frequencies
    names = update_freq(er)
    names = useMajorityLabel(names)
    names = dropDuplicates(names)
#     import pdb; pdb.set_trace()
    final_df = pd.DataFrame()
    final_df['Name'] = names['Name']
    final_df['Gender'] = names['new_labels']
    return final_df

def ERData_MajorityLabel_counts():
    daman = ERStateData_with_freq(DAMAN_CSV)
    manipur = ERStateData_with_freq(MANIPUR_CSV)
    meghalaya = ERStateData_with_freq(MEGHALAYA_CSV)
    nagaland = ERStateData_with_freq(NAGALAND_CSV)
    arunachal =ERStateData_with_freq(ARUNACHAL_CSV)
    delhi = ERStateData_with_freq(DELHI_CSV)
    sikkim = ERStateData_with_freq(SIKKIM_CSV)
    goa = ERStateData_with_freq(GOA_CSV)
    mizoram = ERStateData_with_freq(MIZORAM_CSV)
    er = pd.concat([daman, manipur, meghalaya, nagaland, arunachal, delhi, sikkim, goa, mizoram], ignore_index = True)
    # update frequencies
    names = update_freq(er)
    names = useMajorityLabel(names)
    names = dropDuplicates(names)
#     import pdb; pdb.set_trace()
    return names
