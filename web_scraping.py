import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_free_agents(url,year):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find_all('table')
    # creates a variable for each year
    # ex. data_2011
    data = pd.read_html(str(tables))[0]

    # Take out totals row and cap hit column
    data.drop(data.tail(1).index,inplace=True)
    data['Year'] = year
    data['Player'] = data.iloc[:,0]
    data['Player'] = data['Player'].apply(lambda x: x.replace('.','').replace("'",''))
    data.drop_duplicates(subset='Player',keep='first',inplace=True)
    data.set_index('Player',inplace=True)
    data = data[['From','To','Year','Pos.','Type']]
    return data

def get_stats(url,year):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    data = pd.read_html(str(tables))
    data = data[0]
    data.drop(['Rk','DRB','ORB'],axis=1,inplace=True)
    data.drop_duplicates(subset='Player',keep='first',inplace=True)
    data['Player'] = data['Player'].apply(lambda x: x.replace("'",'')
                                                                                          .replace('.','')
                                                                                          .replace('*',''))
    data.set_index('Player',inplace=True)
    return data

def get_salaries(url,year):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    data = pd.read_html(str(tables))[0]
    data.drop_duplicates(subset='Player',keep='first',inplace=True)
    data['Player'] = data['Player'].apply(lambda x: x.replace("'",'').replace('.',''))
    data.set_index('Player',inplace=True)
    data['Year'] = year
    return data