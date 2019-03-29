import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from collections import defaultdict
import pickle

# Get current year
now = datetime.datetime.now()
this_year = now.year

# Make a request for the data
req = requests.get('https://www.spotrac.com/nba/free-agents/')
req.status_code
# get just the content from the html
content = req.content
soup = BeautifulSoup(content,"lxml")
# Get only the table from the webpage
tables = soup.find_all('table')
# Turn the table to a pandas dataframe
data_2019 = pd.read_html(str(tables))
# Output was a list. Get the dataframe out of the list
data_2019 = data_2019[0]

data_2019['Salary'] = data_2019['2018-2019 AAV']
data_2019.drop(['2018-2019 AAV','Rights'],axis=1,inplace=True)
data_2019['Player'] = data_2019.iloc[:,0]
data_2019.drop(data_2019.iloc[:,0].name,axis=1,inplace=True)
data_2019['Salary'] = data_2019['Salary'].apply(lambda x: x.replace('$','').replace(',',''))
data_2019.set_index('Player',inplace=True)

# list of years to scrape data for
years = list(range(2011,this_year))


# loop through the years to make a new dataframe for each year
for year in years:
    req = requests.get('https://www.spotrac.com/nba/free-agents/' + str(year))
    content = req.content
    soup = BeautifulSoup(content,"lxml")
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
    globals()['data_%s' % year].drop_duplicates(subset='Player',keep='first',inplace=True)
    globals()['data_%s' % year].set_index('Player',inplace=True)


data = []
for year in years:
    data.append(globals()['data_%s' % year])

data=pd.concat(data)

# List of teams that made the playoffs every year
playoffs_2011 = ['IND','MIA','CHI','POR','DAL','PHI','ATL','NYK','SAS','OKC','DEN','LAL','BOS','ORL','CHA','MEM']
playoffs_2012 = ['PHI','CHI','ORL','IND','NYK','MIA','DAL','OKC','BOS','ATL','DEN','LAL','LAC','MEM','UTH','SAS']
playoffs_2013 = ['CHI','BKN','GSW','DEN','MEM','LAC','BOS','NYK','ATL','IND','MIL','MIA','HOU','OKC','LAL','SAS']
playoffs_2014 = ['ATL','IND','GSW','LAC','MEM','OKC','BKN','TOR','WAS','CHI','POR','HOU','CHA','MIA','DAL','SAS']
playoffs_2015 = ['MIL','CHI','NOP','GSW','DAL','HOU','WAS','TOR','BKN','ATL','BOS','CLE','SAS','LAC','POR','MEM']
playoffs_2016 = ['BOS','ATL','HOU','GSW','DAL','OKC','IND','TOR','DET','CLE','POR','LAC','CHA','MIA','MEM','SAS']
playoffs_2017 = ['IND','CLE','UTH','LAC','MEM','SAS','MIL','TOR','CHI','BOS','POR','GSW','OKC','HOU','ATL','WAS']
playoffs_2018 = ['SAS','GSW','MIA','PHI','NOP','POR','WAS','TOR','MIL','BOS','IND','CLE','MIN','HOU','UTH','OKC']

# Get data for players stats for every year
for year in years:
    req = requests.get("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year))
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    globals()['stats_%s' % year] = pd.read_html(str(tables))
    globals()['stats_%s' % year] = globals()['stats_%s' % year][0]
    globals()['stats_%s' % year].drop(['Rk','Age','DRB','ORB'],axis=1,inplace=True)
    globals()['stats_%s' % year].drop_duplicates(subset='Player',keep='first',inplace=True)
    globals()['stats_%s' % year]['Player'] = globals()['stats_%s' % year]['Player'].apply(lambda x: x.replace("'",'')
                                                                                          .replace('.','')
                                                                                          .replace('*',''))
    globals()['stats_%s' % year].set_index('Player',inplace=True)
    globals()['stats_%s' % year]['Year'] = year
    # Add boolean column where 1: team made the playoffs, 0: team did not make the playoffs
    globals()['stats_%s' % year]['Playoffs'] = globals()['stats_%s' % year]['Tm'].apply(lambda x: True if x in globals()['playoffs_%s' % year] else False).astype(int)

stats_data = []
for year in years:
    stats_data.append(globals()['stats_%s' % year])
stats_data = pd.concat(stats_data)

stats_data.rename(index={'JJ Barea': 'Jose Barea'},inplace=True)
salary_data.rename(index={'Jose Juan Barea':'Jose Barea'},inplace=True)
salary_data.rename(index={'Aleksandar Pavlovic':'Sasha Pavlovic'},inplace=True)
salary_data.rename(index={'Hidayet Turkoglu':'Hedo Turkoglu'},inplace=True)
salary_data.rename(index={'Maurice Williams':'Mo Williams'},inplace=True)
salary_data.rename(index={'Nenê':'Nene Hilario'},inplace=True)
salary_data.rename(index={'Kelenna Azubuike':'Kelenna Azubuike'},inplace=True)
salary_data.rename(index={'Predrag Stojakovic':'Peja Stojakovic'},inplace=True)
data.rename(index={'Luc Richard Mbah a Moute':'Luc Mbah a Moute'},inplace=True)
data.rename(index={'John Lucas III':'John Lucas'},inplace=True)


for year in years:
    last = year - 1
    req = requests.get('https://hoopshype.com/salaries/players/{}-{}/'.format(str(last),year))
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    a = pd.read_html(str(tables))
    a = a[0]
    a = a.drop_duplicates(subset='Player',keep='first')
    a.set_index('Player',inplace=True)
    a['Year'] = year
    a['Salary1'] = a['{}/{}'.format(last,str(year)[2:])]
    a['Salary'] = a['Salary1'].apply(lambda x: x.replace('$','').replace(',',''))
    globals()['salary_%s' % year] = a[['Salary','Year']]

salary_data = []
for year in years:
    salary_data.append(globals()['salary_%s' % year])
salary_data = pd.concat(salary_data)


for year in years:
    req = requests.get('https://www.spotrac.com/nba/cap/{}/'.format(year))
    content = req.content
    soup = BeautifulSoup(content,"lxml")
    tables = soup.find('table')
    globals()['team_cap_%s' % year] = pd.read_html(str(tables))
    globals()['team_cap_%s' % year] = globals()['team_cap_%s' % year][0]
    globals()['team_cap_%s' % year] = globals()['team_cap_%s' % year][['Team','Lux Tax Space']]
    globals()['team_cap_%s' % year].set_index('Team')
    globals()['team_cap_%s' % year]['Lux Tax Space'] = globals()['team_cap_%s' % year]['Lux Tax Space'].apply(lambda x: 
                                                                                                              int(x.replace('$','')
                                                                                                                  .replace(',','')
                                                                                                                  .replace('*','')))

team_dict = {'SAC':'Sacramento Kings','IND':'Indiana Pacers','NJN':'New Jersey Nets','HOU':'Houston Rockets'
             ,'TOR':'Toronto Raptors','MIN':'Minnesota Timberwolves','GSW':'Golden State Warriors','UTH':'Utah Jazz'
             ,'NOH':'New Orleans Hornets','CLE':'Cleveland Cavaliers','NYK':'New York Knicks','OKC':'Oklahoma City Thunder'
             ,'DET':'Detroit Pistons','PHI':'Philadelphia 76ers','PHX':'Phoenix Suns','CHA':'Charlotte Hornets'
             ,'POR':'Portland Trail Blazers','MIL':'Milwaukee Bucks','MEM':'Memphis Grizzlies','WAS':'Washington Wizards'
             ,'ORL':'Orlando Magic','LAC':'Los Angeles Clippers','CHI':'Chicago Bulls','ATL':'Atlanta Hawks'
             ,'SAS':'San Antonio Spurs','DAL':'Dallas Mavericks','BOS':'Boston Celtics','MIA':'Miami Heat'
             ,'LAL':'Los Angeles Lakers','DEN':'Denver Nuggets','NOP':'New Orleans Pelicans','BKN':'Brooklyn Nets'}

team_cap_2011['Team'].iloc[15] = 'Charlotte Hornets'
team_cap_2012['Team'].iloc[3] = 'Charlotte Hornets'
team_cap_2012['Team'].iloc[28] = 'Brooklyn Nets'
team_cap_2013['Team'].iloc[8] = 'Charlotte Hornets'
data_2012['From'].iloc[100] = 'BKN'
data_2012['From'].iloc[128] = 'BKN'
data_2012['From'].iloc[132] = 'BKN'
data_2012['From'].iloc[174] = 'BKN'
data_2012['From'].iloc[184] = 'BKN'
data_2012['From'].iloc[209] = 'BKN'
data_2012['From'].iloc[233] = 'BKN'
data_2013['From'].iloc[284] = 'NOP'

for year in years:
    team_cap = []
    for i in range(len(globals()['data_%s' % year])):
        if type(globals()['data_%s' % year].iloc[i]['From']) == float:
            team_cap.append(0)
        else:
            team = team_dict[globals()['data_%s' % year].iloc[i]['From']]
            cap = globals()['team_cap_%s' % year][globals()['team_cap_%s' % year]['Team'] == team]['Lux Tax Space'].iloc[0]
            team_cap.append(cap)
    globals()['data_%s' % year]['Team Cap'] = team_cap

free_agents = defaultdict(pd.DataFrame)
stats = defaultdict(pd.DataFrame)
salary = defaultdict(pd.DataFrame)
team_cap = defaultdict(pd.DataFrame)
for year in years:
    for player in data.index:
        free_agents[player] = data[data.index == player]
        stats[player] = stats_data[stats_data.index == player]
        salary[player] = salary_data[salary_data.index == player]

free_agents_df = pd.DataFrame()
for player in free_agents:
    df = free_agents[player]
    if len(free_agents_df) == 0:
        free_agents_df = df
    else:
        free_agents_df = pd.concat([free_agents_df,df])

stats_df = pd.DataFrame()
for player in stats:
    df = stats[player]
    if len(stats) == 0:
        stats_df = df
    else:
        stats_df = pd.concat([stats_df,df])

salary_df = pd.DataFrame()
for player in salary:
    df = salary[player]
    if len(salary_df) == 0:
        salary_df = df
    else:
        salary_df = pd.concat([salary_df,df])


free_agents_df.to_pickle('data/free_agents.p')
stats_df.to_pickle('data/stats.p')
salary_df.to_pickle('data/salary.p')

if __name__ == "__main__":
    pass