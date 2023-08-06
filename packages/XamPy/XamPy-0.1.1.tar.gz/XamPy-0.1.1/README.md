# XamPy
## Links
- [Code of Conduct](https://github.com/XamNalpak/xampy/blob/main/CODE-OF-CONDUCT.md)
- [Contributing](https://github.com/XamNalpak/xampy/blob/main/CONTRIBUTING.md)
- [Issues](https://github.com/XamNalpak/xampy/issues)
- [License](https://github.com/XamNalpak/xampy/blob/main/LICENSE)


# _Information_


XamPy is a Data Science Package written in Python. 
## Features

- Simplifying the process of analyzing data
- User-Friendly command based sripting package

## Packages Used

XamPy uses a number of open source projects to work properly:

- Pandas - Data manipulation tool for python
- Numpy - awesome tool for matrix/array mathmatics
- MatPlotLib - tool for graphing in python

# Installation
```
pip install xampy
or
pip3 install xampy
```
# Example Use cases
## Reading in data from file path
```
import xampy as xp
path = 'C:\Users\User\Documents\Data\data.csv'

# using makeData() to read in data
data = xp.makeData(path)

# quick statistics and summary of the data at hand
xp.showInfo(data)

# removing white space from column names and insert an underscore
data = xp.renameCols(data,' ','_')

# splitting the data into numerical and nonnumerical sections

numerical,categorical = xp.dataTypeSplit(data)


# Counting nulls in the dataframe, prints the number of missing vals in the DF
xp.CountMissing(data)

# example column money (float) has missing values
data = xp.meanFill(data,'money')

# example column Gender (Binary or text) has missing values
data = xp.modeFill(data,'Gender')

```
if we want to seperate the data into genders
eq=equal
gte=greater than equal to
lte=less than equal to
lt = less than
gt = greater than

FOR STRINGS WE USE 'eq', for any numerical data we can use any comparrison #operator
```
males = xp.SubSetDf(data,'Gender','Male','eq')
females = xp.SubSetDf(data,'Gender','Female','eq')
```


## License

MIT

**Free Software, Hell Yeah!**

