import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




#creates a dataframe from a file path
def makeData(filepath):
    df = pd.read_csv(filepath)
    return df

# prints out quick statistical information
def showInfo(dataframe):
    print(dataframe.describe())
    print("-"*50)
    print(dataframe.info())


def numBarPlot(dataframe, items:list):
    def bar_plot(variable):
        """
            input: variable ex: "Sex"
            output: bar plot & value count
        """
        # get feature
        var = dataframe[variable]
        # count number of categorical variable
        varValue = var.value_counts()
        
        # visualize
        plt.figure(figsize = (9,3))
        plt.bar(varValue.index, varValue)
        plt.xticks(varValue.index, varValue.index.values)
        plt.ylabel("Frequency")
        plt.title(variable)
        plt.show()
        print("{}: \n {}".format(variable, varValue))

    for c in items:
        bar_plot(c)



def catPlots(dataframe,items:list):
    def plot_hist(variable):
        plt.figure(figsize = (9,3))
        plt.hist(dataframe[variable], bins = 50)
        plt.xlabel(variable)
        plt.ylabel("Frequency")
        plt.title("{} distrubution with hist".format(variable))
        plt.show()
    for n in items:
        plot_hist(n)


def countMissing(df):
    print(df.isnull().sum())

def ModeFill(dataframe,colName):
    dataframe[colName] = dataframe[colName].fillna(df[colName].mode()[0])
    return dataframe

def MeanFill(dataframe,colName):
    dataframe[colName] = dataframe[colName].fillna(df[colName].mean().round(3))
    return dataframe


def subSetDf(dataframe,col,value,condition):
    if condition == 'gte':
        df = df[df[col] >= value]
    elif condition == 'lte':
        df = df[df[col] <= value]
    elif condition == 'eq':
        df = df[df[col] == value]
    elif condition == 'gt':
        df = df[df[col] > value]
    elif condition == 'lt':
        df = df[df[col] < value]
    else:
        print(f'{condition} is not a valid selection, choose from the list: \n gt\nlt\gte\nlte\neq')


# takes all things where its not equal to this value        
def OutDF(df,col,val):
    df = df[topics_data[col] != val]
    return df


def renameCols(df,remove,replace):
  df = df.rename(columns=lambda x: x.strip(remove))
  df = df.rename(columns=lambda x: x.replace(' ',replace))
  return df


def dataTypeSplit(df):
    nums = []
    nonnums = []

    for i in df.columns:
      if df[i].dtypes == int or df[i].dtypes == float:
        nums.append(i)
      else:
        nonnums.append(i)

    numdf = df[nums]

    nonnumdf = df[nonnums]

    return numdf,nonnumdf
