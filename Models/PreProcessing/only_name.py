import pandas as pd
import numpy as np

def preprocessOnlyNameData(data_df):
    name_df = pd.DataFrame()
    
    name_df['Name'] = data_df['name']
    name_df['Gender'] = data_df['gender']
    name_df.dropna()
    
    # for now drop the rows that have 
    name_df = name_df.drop_duplicates()
    # considering only 2 genders for now
    name_df = name_df.loc[name_df['Gender'].isin({'MALE','FEMALE'})]
    name_df = name_df.reset_index(drop=True)
    return name_df

