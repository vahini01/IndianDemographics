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

def AIEEECasteData():
  ai10 = pd.read_csv(AIEEE_2010_CSV)
  ai11 = pd.read_csv(AIEEE_2011_CSV)
  ai09 = pd.read_csv(AIEEE_2009_CSV)
  caste_10 = getCaste(ai10, 'category')
  caste_11 = getCaste(ai11, 'category')
  caste_09 = getCaste(ai09, 'category')
  caste_df = pd.concat([caste_09, caste_10, caste_11], ignore_index=True)
  return caste_df

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
    caste_index = {'GEN':[1,0], 'OBC':[0,1], 'SC':[0,1], 'ST':[0,1]}

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

        Y.append(caste_index[caste[i].upper().strip()])
            
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
