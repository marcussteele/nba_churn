import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Get current year
now = datetime.datetime.now()
this_year = now.year

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
    last = year - 1
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

for year in years:
    globals()['free_agent_%s' % year] = pd.concat([globals()['stats_%s' % year],globals()['salary_%s' % year]]
                                                  ,axis=1,sort=False)

for year in years:
    globals()['final_%s' % year] = pd.concat([globals()['data_%s' % year],globals()['free_agent_%s' % year]]
                                             ,axis=1,join_axes=[globals()['data_%s' % year].index])

for year in years:
    req = requests.get('https://www.spotrac.com/nba/cap/{}/'.format(year))
    content = req.content
    soup = BeautifulSoup(content)
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
             ,'DET':'Detroit Pistons','PHI':'Philadelphia 76ers','PHX':'Phoenix Suns','CHA':'Charlotte Bobcats'
             ,'POR':'Portland Trail Blazers','MIL':'Milwaukee Bucks','MEM':'Memphis Grizzlies','WAS':'Washington Wizards'
             ,'ORL':'Orlando Magic','LAC':'Los Angeles Clippers','CHI':'Chicago Bulls','ATL':'Atlanta Hawks'
             ,'SAS':'San Antonio Spurs','DAL':'Dallas Mavericks','BOS':'Boston Celtics','MIA':'Miami Heat'
             ,'LAL':'Los Angeles Lakers','DEN':'Denver Nuggets','NOP':'New Orleans Pelicans','BKN':'Brooklyn Nets'}

data = []
for year in years:
    data.append(globals()['final_%s' % year])

final_data = pd.concat(data)

team_cap = []
for i in range(len(final_data)):
    if type(final_data.iloc[i]['From']) == float:
        team_cap.append(0)
    else:
        team = team_dict[final_data.iloc[i]['From']]
        yr = final_data.iloc[i]['Year of Free Agency']
        cap = globals()['team_cap_%s' % yr][globals()['team_cap_%s' % yr]['Team'] == team]['Lux Tax Space'].iloc[0]
        team_cap.append(cap)
final_data['Team Cap'] = team_cap

final_data.to_pickle('data/final_data.p')

if __name__ == "__main__":
    pass