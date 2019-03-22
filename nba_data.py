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
data_2019 = data_2019

years = ['2011','2012','2013','2014','2015','2016','2017','2018']
for year in years:
    req = requests.get('https://www.spotrac.com/nba/free-agents/' + year)
    content = req.content
    soup = BeautifulSoup(content)
    tables = soup.find_all('table')
    globals()['data_%s' % year] = pd.read_html(str(tables))
    globals()['data_%s' % year] = globals()['data_%s' % year][0]

data = [data_2011,data_2012,data_2013,data_2014,data_2015,data_2016,data_2017,data_2018,data_2019]
length = 0
for dataset in data:
    l = len(dataset[0])
    length += l

