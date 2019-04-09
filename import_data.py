import pandas as pd


def get_data(file):
    '''
    INPUT: Takes in a path to a pickle file that you want to load in.
    
    OUTPUT: Returns a pandas dataframe of the pickle file that was uploaded.
    '''
    data = pd.read_pickle(file)
    return data

def add_features(df):
    df['MP'] = df['MP'].astype(float)
    df['PTS'] = df['PTS'].astype(float)
    new_column = df.groupby('Player',as_index=False,sort=False)['MP'].rolling(3,min_periods=1).mean()
    new_column1 = df.groupby('Player',as_index=False,sort=False)['PTS'].rolling(3,min_periods=1).mean()
    df['Diff MP3'] = df['MP'] - new_column.values
    df['Diff PTS3'] = df['PTS'] - new_column1.values
    df['Traded'] = (df['Tm'] == 'TOT').astype(int)
    df['one'] = 1
    df['Years Same Team'] = df.groupby(['Player','Tm'])['one'].cumsum()
    df.drop('one',axis=1,inplace=True)
    return df

def combine_data(salary_data,stats_data,free_agent_data):
    '''
    INPUT: Takes in all salary data, stats data, and free agent data in that order and 
            combines them into one big dataframe.
    OUTPUT: One pandas dataframe.
    '''
    final_data = pd.DataFrame()
    for player in free_agent_data.index.unique():
        p = free_agent_data[free_agent_data.index==player]
        for i in range(len(p)):
            year = p['Year'].iloc[i]
            df1 = p[p['Year']==year]
            df2 = stats_data[(stats_data.index==player)&(stats_data['Year']==year)]
            df3 = salary_data[(salary_data.index==player)&(salary_data['Year']==year)]
            temp = pd.concat([df1,df2,df3],axis=1,sort=False)
            if len(final_data) == 0:
                final_data = temp
            else:
                final_data = pd.concat([final_data,temp])
    final_data = final_data.loc[:,~final_data.columns.duplicated()]
    return final_data



if __name__ == '__main__':
    pass    