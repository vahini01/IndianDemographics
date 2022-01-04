import pandas as pd
import numpy as np
from split_name import *
from parse_df import *
from utils import *

def splitTrainTest(data_df, percent, col):
    if percent == 1:
        return data_df, pd.DataFrame()
    data_df, first_names = split_name_df(data_df, col) 
    first_names = pd.DataFrame(first_names, columns = ['first_name'])
    first_names = first_names.drop_duplicates()
    train_msk = np.random.rand(len(first_names)) < percent
    train_first_names = first_names[train_msk]
    test_first_names = first_names[~train_msk]
    tmsk = np.ones(len(data_df), dtype=bool)
    for i in range(len(tmsk)):
      if data_df['first_name'][i] in train_first_names['first_name'].tolist():
        tmsk[i] = True
      else :
        tmsk[i] = False 
    train = data_df[tmsk]
    test = data_df[~tmsk]
    return train, test

# Segregating data so that no two people with same first name will belong to train or test data 
def splitTrainTestVal(data_df, percent, val, col):
    '''
    data_df : dataframe that we wish to split
    percent : train % 
    val : validation percentage in train
    col : column name of 'NAME'
    '''
    data_df = data_df.reset_index(drop=True)
    train, test = splitTrainTest(data_df, percent+val, col)
    train, val = splitTrainTest(train, percent/(percent+val), col)
    print(f"(train:{train.shape}, val:{val.shape}, test:{test.shape})")
    return train, val, test
    
def preprocessData(data_df):
    name_df = pd.DataFrame()
    # Ignore these for now, they aren't parsed correctly
    father_df = pd.DataFrame()
    mother_df = pd.DataFrame()
    husband_df = pd.DataFrame()
    name_df['Name'] = data_df['name']
    name_df['Gender'] = data_df['gender']
    name_df.dropna()
    father_df['Name'] = data_df['father_name'].dropna()
    father_df['Gender'] = 'MALE'
    husband_df['Name'] = data_df['husband_name'].dropna()
    husband_df['Gender'] = 'MALE'
    mother_df['Name'] = data_df['mother_name'].dropna()
    mother_df['Gender'] = 'FEMALE'
    name_df = name_df.append(father_df, ignore_index = True)
    name_df = name_df.append(mother_df, ignore_index = True)
    name_df = name_df.append(husband_df, ignore_index = True)
    
    # for now drop the rows that have 
    name_df = name_df.drop_duplicates()
    # considering only 2 genders for now
    name_df = name_df.loc[name_df['Gender'].isin({'MALE','FEMALE'})]
    name_df = name_df.reset_index(drop=True)
    return name_df
