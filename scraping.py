import requests
from bs4 import BeautifulSoup
from web_scraping import get_free_agents, get_salaries, get_stats
import pandas as pd
import datetime
from collections import defaultdict
import os


def main():
# Get current year
    now = datetime.datetime.now()
    this_year = now.year

    # list of years to scrape data for
    years = list(range(2011,this_year+1))

    # loop through the years to make a new dataframe for each year
    data_dict = dict()
    for year in years:
        if year == this_year:
            url = 'https://www.spotrac.com/nba/free-agents/'
            try:
                data = get_free_agents(url,year)
                data_dict['data_%s' % year] = data
            except:
                # Make a request for the data
                req = requests.get(url)
                # get just the content from the html
                content = req.content
                soup = BeautifulSoup(content,"lxml")
                # Get only the table from the webpage
                tables = soup.find_all('table')
                # Turn the table to a pandas dataframe
                data = pd.read_html(str(tables))[0]
                data['Player'] = data.iloc[:,0]
                data.drop_duplicates(subset='Player',keep='first',inplace=True)
                data.set_index('Player',inplace=True)
                data.drop([data.iloc[:,-1].name,data.iloc[:,0].name,'Rights'],axis=1,inplace=True)
                data['From'] = data['Team']
                data['Year'] = year
                data = data[['From','Type','To','Pos.','Year']]
                data_dict['data_%s' % year] = data

        else:
            url = 'https://www.spotrac.com/nba/free-agents/' + str(year)
            data = get_free_agents(url,year)
            data_dict['data_%s' % year] = data


    # List of teams that made the playoffs every year
    playoffs_dict = {'playoffs_2011': ['IND', 'MIA', 'CHI', 'POR', 'DAL', 'PHI', 'ATL', 'NYK', 'SAS', 'OKC', 'DEN', 'LAL', 'BOS', 'ORL', 'CHA', 'MEM'],
                'playoffs_2012': ['PHI', 'CHI', 'ORL', 'IND', 'NYK', 'MIA', 'DAL', 'OKC', 'BOS', 'ATL', 'DEN', 'LAL', 'LAC', 'MEM', 'UTH', 'SAS'],
                'playoffs_2013': ['CHI', 'BKN', 'GSW', 'DEN', 'MEM', 'LAC', 'BOS', 'NYK', 'ATL', 'IND', 'MIL', 'MIA', 'HOU', 'OKC', 'LAL', 'SAS'],
                'playoffs_2014': ['ATL', 'IND', 'GSW', 'LAC', 'MEM', 'OKC', 'BKN', 'TOR', 'WAS', 'CHI', 'POR', 'HOU', 'CHA', 'MIA', 'DAL', 'SAS'],
                'playoffs_2015': ['MIL', 'CHI', 'NOP', 'GSW', 'DAL', 'HOU', 'WAS', 'TOR', 'BKN', 'ATL', 'BOS', 'CLE', 'SAS', 'LAC', 'POR', 'MEM'],
                'playoffs_2016': ['BOS', 'ATL', 'HOU', 'GSW', 'DAL', 'OKC', 'IND', 'TOR', 'DET', 'CLE', 'POR', 'LAC', 'CHA', 'MIA', 'MEM', 'SAS'],
                'playoffs_2017': ['IND', 'CLE', 'UTH', 'LAC', 'MEM', 'SAS', 'MIL', 'TOR', 'CHI', 'BOS', 'POR', 'GSW', 'OKC', 'HOU', 'ATL', 'WAS'],
                'playoffs_2018': ['SAS', 'GSW', 'MIA', 'PHI', 'NOP', 'POR', 'WAS', 'TOR', 'MIL', 'BOS', 'IND', 'CLE', 'MIN', 'HOU', 'UTH', 'OKC'],
                'playoffs_2019': ['MIL', 'TOR', 'PHI', 'BOS', 'ORL', 'IND', 'BKN', 'GSW', 'DEN', 'HOU', 'POR', 'UTH', 'OKC', 'SAS', 'LAC', 'DET'],
                'playoffs_2020': ['MIL', 'TOR', 'PHI', 'BOS', 'ORL', 'MIA', 'IND', 'BKN', 'LAC', 'LAL', 'POR', 'DEN', 'DAL', 'HOU', 'OKC', 'UTH']}

    
    # Get data for players stats for every year
    stats_dict = dict()
    for year in range(2009,this_year+1):
        url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
        data = get_stats(url,year)
        data['Year'] = year
        stats_dict['stats_%s' % year] = data
        
    # Add boolean column where 1: team made the playoffs, 0: team did not make the playoffs
    for year in years[:-1]:
        stats_dict['stats_%s' % year]['Playoffs'] = stats_dict['stats_%s' % year]['Tm'].apply(lambda x: True if x in playoffs_dict['playoffs_%s' % year] else False).astype(int)

    stats_data = pd.concat(stats_dict.values(),sort=False)

    total_cap_dict = {'2010':57700000,'2011':58044000,'2012':58044000,'2013':58044000,'2014':58679000,'2015':63065000
                ,'2016':70000000,'2017':94143000,'2018':99093000,'2019':101869000,'2020':109000000}

    salary_dict = dict()
    for year in years[:-1]:
        if year == this_year:
            url = 'https://hoopshype.com/salaries/players/'
        
        else:
            url = 'https://hoopshype.com/salaries/players/{}-{}/'.format(str(year-1),year)

        data = get_salaries(url,year)
        data['Salary1'] = data['{}/{}'.format(year-1,str(year)[2:])]
        data['Salary'] = data['Salary1'].apply(lambda x: x.replace('$','').replace(',',''))
        data['Total Cap'] = total_cap_dict[str(year)]
        data['Salary %'] = data['Salary'].astype(float) / data['Total Cap']
        salary_dict['salary_%s' % year] = data[['Salary','Salary %','Year']]


    salary_data = pd.concat(salary_dict.values())

    team_cap_dict = dict()
    for year in years:
        req = requests.get('https://www.spotrac.com/nba/cap/{}/'.format(year))
        content = req.content
        soup = BeautifulSoup(content,"lxml")
        tables = soup.find('table')
        team_cap_dict['team_cap_%s' % year] = pd.read_html(str(tables))[0]
        team_cap_dict['team_cap_%s' % year] = team_cap_dict['team_cap_%s' % year][['Team','Lux Tax Space']]
        team_cap_dict['team_cap_%s' % year]['Team'] = team_cap_dict['team_cap_%s' % year]['Team'].apply(lambda x: x[:-3])
        team_cap_dict['team_cap_%s' % year].set_index('Team')
        team_cap_dict['team_cap_%s' % year]['Lux Tax Space'] = team_cap_dict['team_cap_%s' % year]['Lux Tax Space'].apply(lambda x: 
                                                                                                                int(x.replace('$','')
                                                                                                                    .replace(',','')
                                                                                                                    .replace('*','')))

    team_dict = {
        'SAC': 'Sacramento Kings',
        'IND':'Indiana Pacers',
        'NJN':'New Jersey Nets',
        'HOU':'Houston Rockets',
        'TOR': 'Toronto Raptors',
        'MIN':'Minnesota Timberwolves',
        'GSW':'Golden State Warriors',
        'UTH':'Utah Jazz',
        'NOH': 'New Orleans Hornets',
        'CLE':'Cleveland Cavaliers',
        'NYK':'New York Knicks',
        'OKC':'Oklahoma City Thunder',
        'DET': 'Detroit Pistons',
        'PHI':'Philadelphia 76ers',
        'PHX':'Phoenix Suns',
        'CHA':'Charlotte Hornets',
        'POR': 'Portland Trail Blazers',
        'MIL':'Milwaukee Bucks',
        'MEM':'Memphis Grizzlies',
        'WAS':'Washington Wizards',
        'ORL': 'Orlando Magic',
        'LAC':'Los Angeles Clippers',
        'CHI':'Chicago Bulls',
        'ATL':'Atlanta Hawks',
        'SAS': 'San Antonio Spurs',
        'DAL':'Dallas Mavericks',
        'BOS':'Boston Celtics',
        'MIA':'Miami Heat',
        'LAL': 'Los Angeles Lakers',
        'DEN':'Denver Nuggets',
        'NOP':'New Orleans Pelicans',
        'BKN':'Brooklyn Nets'}

    team_cap_dict['team_cap_2011']['Team'].iloc[15] = 'Charlotte Hornets'
    team_cap_dict['team_cap_2012']['Team'].iloc[3] = 'Charlotte Hornets'
    team_cap_dict['team_cap_2012']['Team'].iloc[28] = 'Brooklyn Nets'
    team_cap_dict['team_cap_2013']['Team'].iloc[8] = 'Charlotte Hornets'
    data_dict['data_2012']['From'].iloc[100] = 'BKN'
    data_dict['data_2012']['From'].iloc[128] = 'BKN'
    data_dict['data_2012']['From'].iloc[132] = 'BKN'
    data_dict['data_2012']['From'].iloc[174] = 'BKN'
    data_dict['data_2012']['From'].iloc[184] = 'BKN'
    data_dict['data_2012']['From'].iloc[209] = 'BKN'
    data_dict['data_2012']['From'].iloc[233] = 'BKN'
    data_dict['data_2013']['From'].iloc[284] = 'NOP'

    for year in years:
        team_cap = []
        for i in range(len(data_dict['data_%s' % year])):
            if type(data_dict['data_%s' % year].iloc[i]['From']) == float:
                team_cap.append(0)
            else:
                team = team_dict[data_dict['data_%s' % year].iloc[i]['From']]
                cap = team_cap_dict['team_cap_%s' % year][team_cap_dict['team_cap_%s' % year]['Team'] == team]['Lux Tax Space'].iloc[0]
                team_cap.append(cap)
        data_dict['data_%s' % year]['Team Cap'] = team_cap

    data = pd.concat(data_dict.values())


    # Change names to match dataframes together. Most are foreign names to their US names
    stats_data.rename(index={'Tim Hardaway':'Tim Hardaway Jr'},inplace=True)
    stats_data.rename(index={'Patty Mills':'Patrick Mills'},inplace=True)
    stats_data.rename(index={'Ish Smith':'Ishmael Smith'},inplace=True)
    stats_data.rename(index={'JJ Barea': 'Jose Barea'},inplace=True)
    stats_data.rename(index={'Eugene Jeter':'Pooh Jeter'},inplace=True)
    stats_data.rename(index={'Byron Mullens':'BJ Mullens'},inplace=True)
    stats_data.rename(index={'Glenn Robinson':'Glenn Robinson III'},inplace=True)
    stats_data.rename(index={'Lou Amundson':'Louis Amundson'},inplace=True)
    stats_data.rename(index={'Lou Williams':'Louis Williams'},inplace=True)
    salary_data.rename(index={'Jose Juan Barea':'Jose Barea'},inplace=True)
    salary_data.rename(index={'Aleksandar Pavlovic':'Sasha Pavlovic'},inplace=True)
    salary_data.rename(index={'Hidayet Turkoglu':'Hedo Turkoglu'},inplace=True)
    salary_data.rename(index={'Maurice Williams':'Mo Williams'},inplace=True)
    salary_data.rename(index={'Nenê':'Nene Hilario'},inplace=True)
    salary_data.rename(index={'Moe Harkless':'Maurice Harkless'},inplace=True)
    salary_data.rename(index={'Kelenna Azubuike':'Kelenna Azubuike'},inplace=True)
    salary_data.rename(index={'Predrag Stojakovic':'Peja Stojakovic'},inplace=True)
    data.rename(index={'Luc Richard Mbah a Moute':'Luc Mbah a Moute'},inplace=True)
    salary_data.rename(index={'John Lucas':'John Lucas III'},inplace=True)
    data.rename(index={'Darrun Hilliard II':'Darrun Hilliard'},inplace=True)
    data.rename(index={'Otto Porter Jr':'Otto Porter'},inplace=True)



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
    

if __name__ == "__main__":
    # Create a file to store pickle files in
    os.system("mkdir data")
    main()