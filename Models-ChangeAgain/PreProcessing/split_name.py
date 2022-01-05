import pandas as pd
import numpy as np

# Currently using heuristic (name = first_name + last_name) 
# [ Assuming name to be of format [<First Name> <Last Name>]]
def split_name(name):
    name = str(name)
    # Trim begining spaces
    name = str(name).strip()
    firstname = str(name).split(' ')[0]
    lastname = ' '.join(str(name).split(" ")[1:])
    return firstname, lastname

def split_name_df(df, col):
    first_name = []
    last_name = []
    for name in df[col]:
        f,l = split_name(name)
        first_name.append(f)
        last_name.append(l)
        
    df['first_name'] = first_name
    df['last_name'] = last_name
    return df, first_name
