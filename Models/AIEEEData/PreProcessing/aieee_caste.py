import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split


AIEEE_2009_CSV = "Models/Data/AIEEEData/aieee_2009.csv"
AIEEE_2010_CSV = "Models/Data/AIEEEData/aieee_2010.csv"
AIEEE_2011_CSV = "Models/Data/AIEEEData/aieee_2011.csv"

def getCaste(df, col):
  df[col] = df[col].replace('', np.NaN)
  df1 = df[df[col].notna()]
  # Not taking PH sub category
  df1[col] = [elem.replace("Sub-PH", "") for elem in df1[col]]
  caste_df = pd.DataFrame()
  caste_df['Name'] = df1['name']
  caste_df['Caste'] = df1[col]
  return caste_df

def processDf(df):
  # Update labels
  df['label'] = 1
  labels = []
  # 0 for General and 1 for Reserved.
  for elem in df['Caste']:
    if elem == 'GEN':
      labels.append(0)
    else:
      labels.append(1)

  df['label'] = labels
    
  df['Name'] = [str(name).strip() for name in df['Name']]
  df['Name'] = [name.lower() for name in df['Name']]
  return df

def addFrequency(df):
  df['general_freq'] = df['Name'].map(df[df['label']==0]['Name'].value_counts())
  df['reserved_freq'] = df['Name'].map(df[df['label']==1]['Name'].value_counts())
  return df

def useMajorityLabel(df):
  df['new_labels'] = 0.0
  labels = []
  for i, name in enumerate(df['Name']):
    if np.isnan(df['general_freq'][i]) or df['reserved_freq'][i] > df['general_freq'][i]:
      # labels.append(1) 1 for RESERVED
      df.at[i,'new_labels'] = 1
    else:
      # labels.append(0) 0 for GENERAL
      df.at[i,'new_labels'] = 0
  return df

def dropDuplicates(df):
  df = df.drop_duplicates(subset='Name', keep='last')
  df = df.reset_index(drop=True)
  return df

def AIEEECasteData():
  ai10 = pd.read_csv(AIEEE_2010_CSV)
  ai11 = pd.read_csv(AIEEE_2011_CSV)
  ai09 = pd.read_csv(AIEEE_2009_CSV)
  caste_10 = getCaste(ai10, 'category')
  caste_11 = getCaste(ai11, 'category')
  caste_09 = getCaste(ai09, 'category')
  caste_df = pd.concat([caste_09, caste_10, caste_11], ignore_index=True)
  # Add Majority Label
  caste_df = processDf(caste_df)
  caste_df = addFrequency(caste_df)
  caste_df = useMajorityLabel(caste_df)
  caste_df = dropDuplicates(caste_df)
  # print(caste_df.head(40))
  final_df = pd.DataFrame()
  final_df['Name'] = caste_df['Name']
  final_df['Caste'] = caste_df['new_labels']
  return final_df

def AIEEECasteStateData():
  states = pd.read_csv('Models/Data/AIEEEData/aieee_states.csv')
  states = states.set_index('Code')
  # Use 38 characters as length ( Name #state)
  states['abbr'] = '00'
  count = 0
  for s in iter_all_strings():
    states.abbr.iloc[count] = s
    count += 1
    if (count == 36):
      break

  dic = states.to_dict()
  st = dic['abbr']

  ai10 = pd.read_csv(AIEEE_2010_CSV)
  ai11 = pd.read_csv(AIEEE_2011_CSV)
  ai09 = pd.read_csv(AIEEE_2009_CSV)

  cms_10 = getMarksCasteState(ai10, MAX_2010, st) 
  cms_11 = getMarksCasteState(ai11, MAX_2011, st)
  cms_09 = getMarksCasteState(ai09, MAX_2009, st)

  casre_df = pd.concat([cms_10, cms_09, cms_11], ignore_index=True)
  caste_df = processDf(caste_df)
  caste_df = addFrequency(caste_df)
  caste_df = useMajorityLabel(caste_df)
  caste_df = dropDuplicates(caste_df)
  # print(caste_df.head(40))
  final_df = pd.DataFrame()
  final_df['Name'] = caste_df['Name'] + caste_df['State']
  final_df['Caste'] = caste_df['new_labels']
  return final_df

def vocab():
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    special = [' ']
    vocab = alpha+special+['END']

    return vocab

def getIndexCaste(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))
    # 0 for General.
    # 1 for Reserved.
    # caste_index = {'GEN':[1,0], 'OBC':[0,1], 'SC':[0,1], 'ST':[0,1]}
    caste_index = {0:[1,0], 1:[0,1]}

    X = []
    Y = []
    next_name = False
    
    # Club all the whitespaces
    df['Name'] = [re.sub('[ \t\n]+',' ', str(name)) for name in df['Name']]
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df['Name']]
    caste = df.Caste
    for i in range(len(caste)):
        name = trunc_X[i]
        tmp = []
        for char in str(name):
            if char not in voc:
                with open(file,'a') as f:
                    f.write(name+'\n')
                next_name = True
                break
            else:
                tmp.append(char_index[char])
        if next_name:
            next_name = False
            continue
        for k in range(0,maxlen - len(str(name))):
            tmp.append(char_index["END"])
        X.append(tmp)

        Y.append(caste_index[int(caste[i])])
            
    return np.asarray(X), np.asarray(Y)

def splitCaste(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    train, test = train_test_split(df, train_size=0.7, random_state=42)
    # train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'Models/AIEEEData/'+'caste_df_oov.txt'

    train_x, train_y = getIndexCaste(train, 30, file)
    # val_x, val_y = getIndexCaste(val, 30, file)
    test_x, test_y = getIndexCaste(test, 30, file)
    print(f'Train: ({train_x.shape},{train_y.shape})  Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, test_x, test_y

import itertools
from string import ascii_lowercase

MAX_2010 = 432
MAX_2011 = 360
MAX_2009 = 432

def getIndexCasteMarksState(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    voc = voc + ['#']
    num = ['0','1','2','3','4','5','6','7','8','9']
    voc = voc + num
    char_index = dict((c, i) for i, c in enumerate(voc))
    # caste_index = {'GEN':[1.,0.], 'OBC':[0.,1.], 'SC':[0.,1.], 'ST':[0.,1.]}
    caste_index = {0:[1.,0.], 1:[0.,1.]}
    
    X = []
    Y = []
    Y1 = []
    next_name = False
    marks = df.Marks
    caste = df.Caste
    names = df.Name
    states = df.State
    for i in range(len(marks)):
        name = names[i].lower()
        tmp = []
        name_len = len(str(name))
        # Add extra characters
        for k in range(0,maxlen - name_len):
            tmp.append(char_index["END"])
        for char in str(name):
            if char not in voc:
                with open(file,'a') as f:
                    f.write(name+'\n')
                next_name = True
                break
            else:
                tmp.append(char_index[char])
        if next_name:
            next_name = False
            continue
        
        # Add state
        tmp.append(char_index['#'])
        st = states[i]
        tmp.append(char_index[st[0]])
        tmp.append(char_index[st[1]])
        X.append(tmp)

        Y.append(marks[i])
        Y1.append(caste_index[int(caste[i])])
            
    return np.asarray(X), np.asarray(Y), np.asarray(Y1)

def splitCasteMarksState(df):
    df = df.reset_index(drop=True)
    # 70 30
    train, test = train_test_split(df, train_size=0.7, random_state=42)
    # train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'Models/AIEEEData/'+'aieee_check_marks_df_oov.txt'
    
    train_x, train_y, train_y1 = getIndexCasteMarksState(train, 35, file)
    test_x, test_y, test_y1 = getIndexCasteMarksState(test, 35, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, train_y1, test_x, test_y, test_y1

def getMarksCasteState(df, max_marks, states):
  df = df[df['p1_marks'].notna()]
  df['category'] = df['category'].replace('', np.NaN)
  df = df[df['category'].notna()]
  df['state_no'] = [state.replace("\xa0","") for state in df.state_no]
  df['state_no'] = df.state_no.replace('', np.NaN)
  df = df[df['state_no'].notna()]
  df['state_no'] = [int(state) for state in df.state_no]
  # Not taking PH sub category
  df['category'] = [elem.replace("Sub-PH", "") for elem in df['category']]
  cm_df = pd.DataFrame()
  cm_df['Name'] = df['name']
  cm_df['Caste'] = df['category']
  cm_df['Marks'] = round((df['p1_marks']/max_marks)*10,2)
  cm_df['State'] = df['state_no'].map(states)
  return cm_df

def iter_all_strings():
  num = ['0','1','2','3','4','5','6','7','8','9']
  for s in itertools.product(num, repeat=2):
      yield "".join(s)

def AIEEECasteState():
  states = pd.read_csv('Models/Data/AIEEEData/aieee_states.csv')
  states = states.set_index('Code')
  # Use 38 characters as length ( Name #state)
  states['abbr'] = '00'
  count = 0
  for s in iter_all_strings():
    states.abbr.iloc[count] = s
    count += 1
    if (count == 36):
      break

  dic = states.to_dict()
  st = dic['abbr']

  ai10 = pd.read_csv(AIEEE_2010_CSV)
  ai11 = pd.read_csv(AIEEE_2011_CSV)
  ai09 = pd.read_csv(AIEEE_2009_CSV)

  cms_10 = getMarksCasteState(ai10, MAX_2010, st) 
  cms_11 = getMarksCasteState(ai11, MAX_2011, st)
  cms_09 = getMarksCasteState(ai09, MAX_2009, st)

  cms_df = pd.concat([cms_10, cms_09, cms_11], ignore_index=True)

  return cms_df


