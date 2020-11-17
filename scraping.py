import requests
from bs4 import BeautifulSoup
from web_scraping import get_free_agents, get_salaries, get_stats
from web_scraping import get_current_year_data, get_past_data, get_team_cap
import pandas as pd
import datetime
from collections import defaultdict
import os


def main():
# Get current year
    now = datetime.datetime.now()
    this_year = now.year

    # list of years to scrape data for
    years = list(range(2011, this_year+1))

    # loop through the years to make a new dataframe for each year
    data_dict = dict()
    cur_data_dict = get_current_year_data(this_year)
    for year in years[:-1]:
        year_dict = get_past_data(year)
        data_dict.update(year_dict)
    data_dict.update(cur_data_dict)

    # List of teams that made the playoffs every year
    ''' ***** Find a way to automate all of this ***** '''
    playoffs_dict = {
        'playoffs': {
            '2011': set(['IND', 'MIA', 'CHI', 'POR', 'DAL', 'PHI', 'ATL', 'NYK', 'SAS', 'OKC', 'DEN', 'LAL', 'BOS', 'ORL', 'CHA', 'MEM']),
            '2012': set(['PHI', 'CHI', 'ORL', 'IND', 'NYK', 'MIA', 'DAL', 'OKC', 'BOS', 'ATL', 'DEN', 'LAL', 'LAC', 'MEM', 'UTH', 'SAS']),
            '2013': set(['CHI', 'BKN', 'GSW', 'DEN', 'MEM', 'LAC', 'BOS', 'NYK', 'ATL', 'IND', 'MIL', 'MIA', 'HOU', 'OKC', 'LAL', 'SAS']),
            '2014': set(['ATL', 'IND', 'GSW', 'LAC', 'MEM', 'OKC', 'BKN', 'TOR', 'WAS', 'CHI', 'POR', 'HOU', 'CHA', 'MIA', 'DAL', 'SAS']),
            '2015': set(['MIL', 'CHI', 'NOP', 'GSW', 'DAL', 'HOU', 'WAS', 'TOR', 'BKN', 'ATL', 'BOS', 'CLE', 'SAS', 'LAC', 'POR', 'MEM']),
            '2016': set(['BOS', 'ATL', 'HOU', 'GSW', 'DAL', 'OKC', 'IND', 'TOR', 'DET', 'CLE', 'POR', 'LAC', 'CHA', 'MIA', 'MEM', 'SAS']),
            '2017': set(['IND', 'CLE', 'UTH', 'LAC', 'MEM', 'SAS', 'MIL', 'TOR', 'CHI', 'BOS', 'POR', 'GSW', 'OKC', 'HOU', 'ATL', 'WAS']),
            '2018': set(['SAS', 'GSW', 'MIA', 'PHI', 'NOP', 'POR', 'WAS', 'TOR', 'MIL', 'BOS', 'IND', 'CLE', 'MIN', 'HOU', 'UTH', 'OKC']),
            '2019': set(['MIL', 'TOR', 'PHI', 'BOS', 'ORL', 'IND', 'BKN', 'GSW', 'DEN', 'HOU', 'POR', 'UTH', 'OKC', 'SAS', 'LAC', 'DET']),
            '2020': set(['MIL', 'TOR', 'PHI', 'BOS', 'ORL', 'MIA', 'IND', 'BKN', 'LAC', 'LAL', 'POR', 'DEN', 'DAL', 'HOU', 'OKC', 'UTH'])
        },
        'finals': {
            '2011': set(['DAL', 'MIA']),
            '2012': set(['OKC', 'MIA']),
            '2013': set(['SAS', 'MIA']),
            '2014': set(['SAS', 'MIA']),
            '2015': set(['GSW', 'CLE']),
            '2016': set(['GSW', 'CLE']),
            '2017': set(['GSW', 'CLE']),
            '2018': set(['GSW', 'CLE']),
            '2019': set(['TOR', 'GSW']),
            '2020': set(['LAL', 'MIA']),
        },
        'champion': {
            '2011': 'DAL',
            '2012': 'MIA',
            '2013': 'MIA',
            '2014': 'SAS',
            '2015': 'GSW',
            '2016': 'CLE',
            '2017': 'GSW',
            '2018': 'GSW',
            '2019': 'TOR',
            '2020': 'LAL',
        }
    }
    
    # Get data for players stats for every year
    stats_dict = dict()
    for year in range(2009, this_year+1):
        data = get_stats(year)
        stats_dict[f'stats_{year}'] = data
        
    # Add boolean column where 1: team made the playoffs, 0: team did not make the playoffs
    for year in years[:-1]:
        stats_dict[f'stats_{year}']['Playoffs'] = stats_dict[f'stats_{year}']['Tm'].apply(lambda x: True if x in playoffs_dict['playoffs'][year] else False).astype(int)

    stats_data = pd.concat(stats_dict.values(), sort=False)

    team_cap_dict = dict()
    total_cap_dict = dict()
    for year in years:
        team_yearly_cap, total_cap = get_team_cap(year)
        team_cap_dict.update(team_yearly_cap)
        total_cap_dict[str(year)] = total_cap


    salary_dict = dict()
    for year in years[:-1]:
        if year == this_year:
            url = 'https://hoopshype.com/salaries/players/'
        else:
            url = 'https://hoopshype.com/salaries/players/{}-{}/'.format(str(year-1), year)

        data = get_salaries(url, year, total_cap_dict)
        salary_dict[year] = data[['Salary', 'Salary %', 'Year']]

    salary_data = pd.concat(salary_dict.values())

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

    team_cap_dict['2011']['Team'].iloc[15] = 'Charlotte Hornets'
    team_cap_dict['2012']['Team'].iloc[3] = 'Charlotte Hornets'
    team_cap_dict['2012']['Team'].iloc[28] = 'Brooklyn Nets'
    team_cap_dict['2013']['Team'].iloc[8] = 'Charlotte Hornets'
    data_dict['2012']['From'].iloc[100] = 'BKN'
    data_dict['2012']['From'].iloc[128] = 'BKN'
    data_dict['2012']['From'].iloc[132] = 'BKN'
    data_dict['2012']['From'].iloc[174] = 'BKN'
    data_dict['2012']['From'].iloc[184] = 'BKN'
    data_dict['2012']['From'].iloc[209] = 'BKN'
    data_dict['2012']['From'].iloc[233] = 'BKN'
    data_dict['2013']['From'].iloc[284] = 'NOP'

    for year in years:
        team_cap = []
        for i in range(len(data_dict[str(year)])):
            if type(data_dict[str(year)].iloc[i]['From']) == float:
                team_cap.append(0)
            else:
                team = team_dict[data_dict[str(year)].iloc[i]['From']]
                cap = team_cap_dict[str(year)][team_cap_dict[str(year)]['Team'] == team]['Lux Tax Space'].iloc[0]
                team_cap.append(cap)
        data_dict[str(year)]['Team Cap'] = team_cap

    data = pd.concat(data_dict.values())


    # Change names to match dataframes together. Most are foreign names to their US names
    stats_data.rename(index={'Tim Hardaway': 'Tim Hardaway Jr'}, inplace=True)
    stats_data.rename(index={'Patty Mills': 'Patrick Mills'}, inplace=True)
    stats_data.rename(index={'Ish Smith': 'Ishmael Smith'}, inplace=True)
    stats_data.rename(index={'JJ Barea': 'Jose Barea'}, inplace=True)
    stats_data.rename(index={'Eugene Jeter': 'Pooh Jeter'}, inplace=True)
    stats_data.rename(index={'Byron Mullens': 'BJ Mullens'}, inplace=True)
    stats_data.rename(index={'Glenn Robinson': 'Glenn Robinson III'}, inplace=True)
    stats_data.rename(index={'Lou Amundson': 'Louis Amundson'}, inplace=True)
    stats_data.rename(index={'Lou Williams': 'Louis Williams'}, inplace=True)
    salary_data.rename(index={'Jose Juan Barea': 'Jose Barea'}, inplace=True)
    salary_data.rename(index={'Aleksandar Pavlovic': 'Sasha Pavlovic'}, inplace=True)
    salary_data.rename(index={'Hidayet Turkoglu': 'Hedo Turkoglu'}, inplace=True)
    salary_data.rename(index={'Maurice Williams': 'Mo Williams'}, inplace=True)
    salary_data.rename(index={'Nenê': 'Nene Hilario'}, inplace=True)
    salary_data.rename(index={'Moe Harkless': 'Maurice Harkless'}, inplace=True)
    salary_data.rename(index={'Kelenna Azubuike': 'Kelenna Azubuike'}, inplace=True)
    salary_data.rename(index={'Predrag Stojakovic': 'Peja Stojakovic'}, inplace=True)
    data.rename(index={'Luc Richard Mbah a Moute': 'Luc Mbah a Moute'}, inplace=True)
    salary_data.rename(index={'John Lucas': 'John Lucas III'}, inplace=True)
    data.rename(index={'Darrun Hilliard II': 'Darrun Hilliard'}, inplace=True)
    data.rename(index={'Otto Porter Jr': 'Otto Porter'}, inplace=True)



    free_agents = defaultdict(pd.DataFrame)
    stats = defaultdict(pd.DataFrame)
    salary = defaultdict(pd.DataFrame)
    team_cap = defaultdict(pd.DataFrame)
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
            free_agents_df = pd.concat([free_agents_df, df])

    stats_df = pd.DataFrame()
    for player in stats:
        df = stats[player]
        if len(stats) == 0:
            stats_df = df
        else:
            stats_df = pd.concat([stats_df, df])

    salary_df = pd.DataFrame()
    for player in salary:
        df = salary[player]
        if len(salary_df) == 0:
            salary_df = df
        else:
            salary_df = pd.concat([salary_df, df])
    

if __name__ == "__main__":
    # Create a file to store pickle files in
    os.system("mkdir data")
    main()