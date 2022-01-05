import pandas as pd
import numpy as np

CBSE_2014 = "Models/Data/CBSEData/2014_complete_data.csv"
CBSE_2015 = "Models/Data/CBSEData/2015_complete_data.csv"

def getParentsData(df):
  mother_df = pd.DataFrame()
  father_df = pd.DataFrame()
  mother_df['Name'] = df['mother_name']
  mother_df['Gender'] = 'FEMALE'
  father_df['Name'] = df['father_name']
  father_df['Gender'] = 'MALE'
  name_df = pd.concat([mother_df, father_df], ignore_index=True)
  return name_df

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
  df = df.reset_index(drop=True)
  return df

def CBSEData():
  cbse14 = pd.read_csv(CBSE_2014)
  cbse15 = pd.read_csv(CBSE_2015)
  c14 = processDf(getParentsData(cbse14))
  c15 = processDf(getParentsData(cbse15))
  cbse = pd.concat([c14, c15], ignore_index=True)
  # Use majority label
  cbse = addFrequency(cbse)
  cbse = useMajorityLabel(cbse)
  cbse = dropDuplicates(cbse)
  final_df = pd.DataFrame()
  final_df['Name'] = cbse['Name']
  final_df['Gender'] = cbse['new_labels']
  return final_df