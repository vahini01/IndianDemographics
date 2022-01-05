from split_name import *
from parse_df import *
from utils import *
import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split

MAXLEN_NAME_CHAR_LSTM = 30
MAXLEN_NAME_CHAR_CNN = 30
NAME = 'Name'
GENDER = 'Gender'

def getVocab():
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    number = ['0','1','2','3','4','5','6','7','8','9']
    special = ['-',',','.',';','!','?',':','`','/','\\','|','_','@','#','$','^','%','&','*','+','=','<','>','(',')','[',']','{','}','~','\'','"', ' ']
    vocab = alpha+number+special + ['END', 'OOV']

    return vocab

def vocab():
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    special = [' ']
    vocab = alpha+special+['END']

    return vocab

def oneHot(i, size):
    tmp = np.zeros(size);
    tmp[i] = 1
    return tmp

def charVocabIndex():
    vocab = getVocab()
    char_index = dict((c, i) for i, c in enumerate(vocab))
    return char_index, len(vocab)

def oneHotEncode(df, Name, Gender, maxlen):
    '''
    #take input upto max and truncate rest
    #encode to vector space(one hot encoding)
    #padd 'END' to shorter sequences
    #also convert each index to one-hot encoding
    '''
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)
    
    char_index, size = charVocabIndex()
    vocab = getVocab()
    X = []
    Y = []
    next_name = False
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df[Name]]
    gender = df[Gender]
    for i in range(len(gender)):
        name = trunc_X[i]
        tmp = []
        for char in str(name):
            if char not in vocab:
                with open('oov_names.txt','a') as f:
                    f.write(name+'\n')
#                 print(name)
                next_name = True
                break
            else:
                tmp.append(oneHot(char_index[char],size))
        if next_name:
            next_name = False
            continue
        for k in range(0,maxlen - len(str(name))):
            tmp.append(oneHot(char_index["END"], size))
        X.append(tmp)

        if str(gender[i]) == 'Boy' or str(gender[i]).lower()=='male':
            Y.append([1,0])
        else:
            Y.append([0,1])
            
    return np.asarray(X), np.asarray(Y) 

def getIndex(df, maxlen, file):
    '''
    #take input upto max and truncate rest
    #encode to vector space(one hot encoding)
    #padd 'END' to shorter sequences
    #also convert each name to list of indices that can be passed onto 
    '''
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))
#     print(voc)
    
    X = []
    Y = []
    next_name = False
    
    # Club all the whitespaces
    df[NAME] = [re.sub('[ \t\n]+',' ', str(name)) for name in df[NAME]]
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df[NAME]]
    gender = df[GENDER]
    for i in range(len(gender)):
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

        if str(gender[i]) == 'Boy' or str(gender[i]).lower()=='male' or gender[i] == 1.0:
            Y.append([1,0])
        else:
            Y.append([0,1])
            
    return np.asarray(X), np.asarray(Y) 

def splitData_oneHot(data_df, percent, val, col):
    train, val, test = splitTrainTestVal(data_df, percent , val, col)
    train_x, train_y = oneHotEncode(train, NAME, GENDER, MAXLEN_NAME_CHAR_LSTM)
    val_x, val_y = oneHotEncode(val, NAME, GENDER, MAXLEN_NAME_CHAR_LSTM)
    test_x, test_y = oneHotEncode(test, NAME, GENDER, MAXLEN_NAME_CHAR_LSTM)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, val_x, val_y, test_x, test_y

def splitData(data_df, percent, val, col, file):
    train, val, test = splitTrainTestVal(data_df, percent , val, col)
    train_x, train_y = getIndex(train, MAXLEN_NAME_CHAR_LSTM, file)
    val_x, val_y = getIndex(val, MAXLEN_NAME_CHAR_LSTM, file)
    test_x, test_y = getIndex(test, MAXLEN_NAME_CHAR_LSTM, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, val_x, val_y, test_x, test_y

def splitERData(data_df, col, file):
#     train, val, test = splitTrainTestVal(data_df, percent , val, col)
    train, test = train_test_split(data_df, test_size=0.3)
    train_x, train_y = getIndex(train, MAXLEN_NAME_CHAR_LSTM, file)
    test_x, test_y = getIndex(test, MAXLEN_NAME_CHAR_LSTM, file)
    print(f'Train: ({train_x.shape},{train_y.shape})  Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, test_x, test_y
