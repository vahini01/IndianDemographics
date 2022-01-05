import pandas as pd
import numpy as np
from char_utils import *
from sklearn.model_selection import train_test_split

MAX_2010 = 432
MAX_2011 = 360
MAX_2009 = 432

def preprocess_aieee(df):
    del df['Unnamed: 0']
    df['category'] = [elem.replace("Category:", "") for elem in df.category]
#     df['category'] = [elem.replace("Sub-\xa0\xa0PH", "") for elem in df.category]
    df['category'] = [elem.replace("\xa0", "") for elem in df.category]
    df['category'] = [elem.replace("\r\n", "") for elem in df.category]
    df.category = [elem.strip() for elem in df.category]
    df['state_no'] = [elem.replace('State Code of Eligibility:','') for elem in df['state_no']]
    # Preprocess marks
    df['p2_marks']=[str(elem).replace('\r\n\r\nNot Applicable/Not Applied\r\n\r\n','?') for elem in df.p2_marks]
    df['p2_marks'] = [str(elem).strip() for elem in df.p2_marks]
    df.p2_marks = df['p2_marks'].replace('nan', np.NaN)
    df.p2_marks = df['p2_marks'].replace('?', np.NaN)
    df['p1_marks'] = [str(elem).strip() for elem in df.p1_marks]
    df['p1_marks']=[str(elem).replace('\r\n','') for elem in df.p1_marks]
    df['p1_marks']=[str(elem).replace('Not Applicable/Not Applied','?') for elem in df.p1_marks]
    # For now replacing ABS with NaN
    df['p1_marks']=[str(elem).replace('ABS','?') for elem in df.p1_marks]
    df.p1_marks = df['p1_marks'].replace('nan', np.NaN)
    df.p1_marks = df['p1_marks'].replace('?', np.NaN)
    df.p1_marks = pd.to_numeric(df.p1_marks)
    df.p2_marks = pd.to_numeric(df.p2_marks)
    return df

def convertMarks(df, col, max_marks):
    df[col] = round((df[col]/max_marks)*10,2)
    return df

# Consider only those students with p1_marks
def getGenderNames(df):
    gender_df = pd.DataFrame()
    father_df = pd.DataFrame()
    mother_df = pd.DataFrame()
    mother_df['Name'] = df['mother_name']
    mother_df['Gender'] = 'FEMALE'
    father_df['Name'] = df['father_name']
    father_df['Gender'] = 'MALE'
    gender_df = gender_df.append(father_df, ignore_index = True)
    gender_df = gender_df.append(mother_df, ignore_index = True)
    return gender_df

def getMarks(df, col, max_marks):
    df1 = df[df[col].notna()]
    marks_df = pd.DataFrame()
    marks_df['Name'] = df1['name']
    marks_df['Marks'] = round((df1[col]/max_marks)*10,2)
    return marks_df

def getMarksCaste(df, max_marks):
    df = df[df['p1_marks'].notna()]
    df['category'] = df['category'].replace('', np.NaN)
    df = df[df['category'].notna()]
    # Not taking PH sub category
    df['category'] = [elem.replace("Sub-PH", "") for elem in df['category']]
    cm_df = pd.DataFrame()
    cm_df['Name'] = df['name']
    cm_df['Caste'] = df['category']
    cm_df['Marks'] = round((df['p1_marks']/max_marks)*10,2)
    return cm_df

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
    
def getCaste(df, col):
    df[col] = df[col].replace('', np.NaN)
    df1 = df[df[col].notna()]
    # Not taking PH sub category
    df1[col] = [elem.replace("Sub-PH", "") for elem in df1[col]]
    caste_df = pd.DataFrame()
    caste_df['Name'] = df1['name']
    caste_df['Caste'] = df1[col]
    return caste_df

def getIndexMarks(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))

    X = []
    Y = []
    next_name = False
    
    # Club all the whitespaces
    df['Name'] = [re.sub('[ \t\n]+',' ', str(name)) for name in df['Name']]
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df['Name']]
    marks = df.Marks
    for i in range(len(marks)):
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

        Y.append(marks[i])
            
    return np.asarray(X), np.asarray(Y)

def getIndexCaste(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))
    caste_index = {'GEN':0, 'OBC':1, 'SC':2, 'ST':3}

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

def getIndexGender(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))
    gender_index = {'FEMALE':0, 'MALE':1}

    X = []
    Y = []
    next_name = False
    
    # Club all the whitespaces
    df['Name'] = [re.sub('[ \t\n]+',' ', str(name)) for name in df['Name']]
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df['Name']]
    gender = df.Gender
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

        Y.append(gender_index[gender[i].upper().strip()])
            
    return np.asarray(X), np.asarray(Y)
                           
def splitMarks(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    trainv, test = train_test_split(df, train_size=0.8, random_state=42)
    train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'marks_df_oov.txt'
    
    train_x, train_y = getIndexMarks(train, 30, file)
    val_x, val_y = getIndexMarks(val, 30, file)
    test_x, test_y = getIndexMarks(test, 30, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, val_x, val_y, test_x, test_y

    
def splitCaste(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    trainv, test = train_test_split(df, train_size=0.8, random_state=42)
    train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'caste_df_oov.txt'

    train_x, train_y = getIndexCaste(train, 30, file)
    val_x, val_y = getIndexCaste(val, 30, file)
    test_x, test_y = getIndexCaste(test, 30, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, val_x, val_y, test_x, test_y
    
    
def splitGender(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    trainv, test = train_test_split(df, train_size=0.8, random_state=42)
    train, val = train_test_split(trainv, test_size=0.875, random_state=42)
    file = 'gender_df_oov.txt'
    
    train_x, train_y = getIndexGender(train, 30, file)
    val_x, val_y = getIndexGender(val, 30, file)
    test_x, test_y = getIndexGender(test, 30, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, val_x, val_y, test_x, test_y
    
    
def getIndexCasteMarks(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    char_index = dict((c, i) for i, c in enumerate(voc))
    caste_index = {'GEN':[1.,0.,0.,0.], 'OBC':[0.,1.,0.,0.], 'SC':[0.,0.,1.,0.], 'ST':[0.,0.,0.,1.]}
    

    X = []
    Y = []
    Y1 = []
    next_name = False
    
    # Club all the whitespaces
    df['Name'] = [re.sub('[ \t\n]+',' ', str(name)) for name in df['Name']]
    
    trunc_X = [str(i).lower()[0:maxlen] for i in df['Name']]
    marks = df.Marks
    caste = df.Caste
    for i in range(len(marks)):
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

        Y.append(marks[i])
        Y1.append(caste_index[caste[i].upper().strip()])
            
    return np.asarray(X), np.asarray(Y), np.asarray(Y1)

def splitCasteMarks(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    trainv, test = train_test_split(df, train_size=0.8, random_state=42)
    train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'marks_df_oov.txt'
    
    train_x, train_y, train_y1 = getIndexCasteMarks(train, 30, file)
    val_x, val_y, val_y1 = getIndexCasteMarks(val, 30, file)
    test_x, test_y, test_y1 = getIndexCasteMarks(test, 30, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, train_y1, val_x, val_y, val_y1, test_x, test_y, test_y1

def getIndexCasteMarksState(df, maxlen, file):
    if df.shape == (0,0):
        return np.empty(0), np.empty(0)
    
    df = df.reset_index(drop=True)

    voc = vocab()
    voc = voc + ['#']
    num = ['0','1','2','3','4','5','6','7','8','9']
    voc = voc + num
    char_index = dict((c, i) for i, c in enumerate(voc))
    caste_index = {'GEN':[1.,0.], 'OBC':[0.,1.], 'SC':[0.,1.], 'ST':[0.,1.]}
    

    X = []
    Y = []
    Y1 = []
    next_name = False
    
    # Club all the whitespaces
    # df['Name'] = [re.sub('[ \t\n]+',' ', str(name)) for name in df['Name']]
    
    # trunc_X = [str(i).lower()[0:maxlen] for i in df['Name']]
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
        Y1.append(caste_index[caste[i].upper().strip()])
            
    return np.asarray(X), np.asarray(Y), np.asarray(Y1)

def splitCasteMarksState(df):
    df = df.reset_index(drop=True)
    # 70 10 20
    trainv, test = train_test_split(df, train_size=0.8, random_state=42)
    train, val = train_test_split(trainv, train_size=0.875, random_state=42)
    file = 'aieee_check_marks_df_oov.txt'
    
    train_x, train_y, train_y1 = getIndexCasteMarksState(train, 35, file)
    val_x, val_y, val_y1 = getIndexCasteMarksState(val, 35, file)
    test_x, test_y, test_y1 = getIndexCasteMarksState(test, 35, file)
    print(f'Train: ({train_x.shape},{train_y.shape}) Val:({val_x.shape},{val_y.shape}) Test: ({test_x.shape},{test_y.shape})')
    return train_x, train_y, train_y1, val_x, val_y, val_y1, test_x, test_y, test_y1

