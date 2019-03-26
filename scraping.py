import requests
from bs4 import BeautifulSoup
import pandas as pd

# Make a request for the data
req = requests.get('https://www.spotrac.com/nba/free-agents/')
req.status_code
# get just the content from the html
content = req.content
soup = BeautifulSoup(content)
# Get only the table from the webpage
tables = soup.find_all('table')
# Turn the table to a pandas dataframe
data_2019 = pd.read_html(str(tables))
# Output was a list. Get the dataframe out of the list
data_2019 = data_2019[0]

# list of years to scrape data for
years = ['2011','2012','2013','2014','2015','2016','2017','2018']

# loop through the years to make a new dataframe for each year
for year in years:
    req = requests.get('https://www.spotrac.com/nba/free-agents/' + year)
    content = req.content
    soup = BeautifulSoup(content)
    tables = soup.find_all('table')
    # creates a variable for each year
    # ex. data_2011
    globals()['data_%s' % year] = pd.read_html(str(tables))
    globals()['data_%s' % year] = globals()['data_%s' % year][0]
    # Take out totals row and cap hit column
    globals()['data_%s' % year].drop(globals()['data_%s' % year].tail(1).index,inplace=True)
    globals()['data_%s' % year].drop(['{} Cap Hit'.format(year),'Dollars'],axis=1,inplace=True)
    globals()['data_%s' % year]['Year of Free Agency'] = year
    globals()['data_%s' % year]['Player'] = globals()['data_%s' % year].iloc[:,0]
    globals()['data_%s' % year]['Player'] = globals()['data_%s' % year]['Player'].apply(lambda x: x.replace('.',''))
    globals()['data_%s' % year].drop(globals()['data_%s' % year].iloc[:,0].name,axis=1,inplace=True)
    globals()['data_%s' % year].set_index('Player',inplace=True)

data_2019['Avg. Salary'] = data_2019['2018-2019 AAV']
data_2019.drop(['2018-2019 AAV','Rights'],axis=1,inplace=True)


# Get data for players stats for every year
for year in years:
    req = requests.get("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year))
    content = req.content
    soup = BeautifulSoup(content)
    tables = soup.find('table')
    globals()['stats_%s' % year] = pd.read_html(str(tables))
    globals()['stats_%s' % year] = globals()['stats_%s' % year][0]
    globals()['stats_%s' % year].drop(['Rk','Age','DRB','ORB'],axis=1,inplace=True)
    globals()['stats_%s' % year].drop_duplicates(subset='Player',keep='first',inplace=True)
    globals()['stats_%s' % year]['Player'] = globals()['stats_%s' % year]['Player'].apply(lambda x: x.replace("'",'')
                                                                                          .replace('.','')
                                                                                          .replace('*',''))
    globals()['stats_%s' % year].set_index('Player',inplace=True)


for year in years:
    last = int(year) - 1
    req = requests.get('https://hoopshype.com/salaries/players/{}-{}/'.format(str(last),year))
    content = req.content
    soup = BeautifulSoup(content)
    tables = soup.find('table')
    a = pd.read_html(str(tables))
    a = a[0]
    a = a.drop_duplicates(subset='Player',keep='first')
    a.set_index('Player',inplace=True)
    globals()['salary_%s' % year] = pd.Series(data=a.iloc[:,1].apply(lambda x: x.replace(',','').replace('$','')))
    globals()['salary_%s' % year].rename('Salary',inplace=True)

