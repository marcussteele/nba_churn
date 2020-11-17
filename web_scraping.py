import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_free_agents(url, year):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content, "lxml")
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
    data = data[['From', 'To', 'Year', 'Pos.', 'Type']]
    return data

def get_stats(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    data = pd.read_html(str(tables))
    data = data[0]
    data.drop(['Rk', 'DRB', 'ORB'],axis=1, inplace=True)
    data.drop_duplicates(subset='Player', keep='first', inplace=True)
    data['Player'] = data['Player'].apply(lambda x: x.replace("'",'')
                                                                                          .replace('.','')
                                                                                          .replace('*',''))
    data['Year'] = year
    data.set_index('Player',inplace=True)
    return data

def get_salaries(url, year, total_cap_dict):
    req = requests.get(url)
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    data = pd.read_html(str(tables))[0]
    data.drop_duplicates(subset='Player', keep='first', inplace=True)
    data['Player'] = data['Player'].apply(lambda x: x.replace("'",'').replace('.',''))
    data.set_index('Player',inplace=True)
    data['Year'] = year
    data['Salary1'] = data['{}/{}'.format(year-1, str(year)[2:])]
    data['Salary'] = data['Salary1'].apply(lambda x: x.replace('$','').replace(',',''))
    data['Total Cap'] = total_cap_dict[str(year)]
    data['Salary %'] = data['Salary'].astype(float) / data['Total Cap']
    return data

def get_current_year_data(this_year):
        data_dict = dict()
        url = 'https://www.spotrac.com/nba/free-agents/'
        try:
            data = get_free_agents(url, this_year)
            data_dict[f'data_{year}'] = data
        except:
            # Make a request for the data
            req = requests.get(url)
            # get just the content from the html
            content = req.content
            soup = BeautifulSoup(content, "lxml")
            # Get only the table from the webpage
            tables = soup.find_all('table')
            # Turn the table to a pandas dataframe
            data = pd.read_html(str(tables))[0]
            data['Player'] = data.iloc[:,0]
            data.drop_duplicates(subset='Player', keep='first', inplace=True)
            data.set_index('Player', inplace=True)
            data.drop([data.iloc[:,-1].name, data.iloc[:,0].name, 'Rights'], axis=1, inplace=True)
            data['From'] = data['Team']
            data['Year'] = this_year
            data = data[['From', 'Type', 'To', 'Pos.', 'Year']]
            data_dict[f'data_{this_year}'] = data
        return data_dict

def get_past_data(year):
    data_dict = dict()
    url = 'https://www.spotrac.com/nba/free-agents/' + str(year)
    data = get_free_agents(url, year)
    data_dict[f'data_{year}'] = data
    return data_dict


def get_team_cap(year):
    team_cap_dict = dict()
    req = requests.get(f'https://www.spotrac.com/nba/cap/{year}/')
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    table_df = pd.read_html(str(tables))[0]
    overall_cap = table_df.iloc[0]['Total Cap'] - table_df.iloc[0]['Cap Space*']
    team_cap_dict[str(year)] = table_df
    team_cap_dict[str(year)] = team_cap_dict[str(year)][['Team', 'Lux Tax Space']]
    team_cap_dict[str(year)]['Team'] = team_cap_dict[str(year)]['Team'].apply(lambda x: x[:-3])
    team_cap_dict[str(year)].set_index('Team')
    team_cap_dict[str(year)]['Lux Tax Space'] = \
        team_cap_dict[str(year)]['Lux Tax Space'].apply(
            lambda x: int(x.replace('$','').replace(',','').replace('*','')))
    return team_cap_dict, overall_cap