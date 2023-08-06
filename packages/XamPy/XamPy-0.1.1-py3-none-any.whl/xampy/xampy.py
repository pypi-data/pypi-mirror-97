import pandas as pd
import numpy as np

def makeCSV(filepath):
    df = pd.read_csv(filepath)
    return df

def showInfo(dataframe):
    print(dataframe.describe())
    print("-"*50)
    print(dataframe.info())

def NumericalPivot(dataframe,features,target):
    dataframe[[features]].groupby([target], as_index=False).mean().sort_values(by=target, ascending=False)

def sexBin(datframe,genderCol):
    dataframe[genderCol] = dataframe[genderCol].map( {'female': 1, 'male': 0} ).astype(int)
    return dataframe