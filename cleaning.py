import pandas as pd


def cleaning(df):
    change_type_data(df)
    final_df = drop_duplicates_useless(df)
    return final_df

def change_type_data(df):
    df['Churn'] = (df['From'] != df['To']).astype(int)
    df['PTS'] = df['PTS'].astype(float)
    df['PF'] = df['PF'].astype(float)
    df['TOV'] = df['TOV'].astype(float)
    df['Age'] = df['Age'].astype(float)
    df['BLK'] = df['BLK'].astype(float)
    df['STL'] = df['STL'].astype(float)
    df['AST'] = df['AST'].astype(float)
    df['TRB'] = df['TRB'].astype(float)
    df['FT%'] = df['FT%'].astype(float)
    df['FTA'] = df['FTA'].astype(float)
    df['FT'] = df['FT'].astype(float)
    df['eFG%'] = df['eFG%'].astype(float)
    df['2P%'] = df['2P%'].astype(float)
    df['2PA'] = df['2PA'].astype(float)
    df['2P'] = df['2P'].astype(float)
    df['3P%'] = df['3P%'].astype(float)
    df['3PA'] = df['3PA'].astype(float)
    df['3P'] = df['3P'].astype(float)
    df['FG%'] = df['FG%'].astype(float)
    df['FGA'] = df['FGA'].astype(float)
    df['FG'] = df['FG'].astype(float)
    df['MP'] = df['MP'].astype(float)
    df['GS'] = df['GS'].astype(float)
    df['G'] = df['G'].astype(float)
    df['Salary'] = df['Salary'].astype(float)
    df['Type'] = df['Type'].astype('category')
    df['Pos.'] = df['Pos.'].astype('category')
    df['Type'] = df['Type'].apply(lambda x: 'RFA' if x == 'CO' else x).apply(lambda x: 'UFA' if x == 'PO' else x)

def drop_duplicates_useless(df):
    df = df.loc[:,~df.columns.duplicated()]
    df.drop(['Pos','To','From'],axis=1,inplace=True)
    df.drop(['3P%','2P%','FT%','FG%','eFG%'],axis=1,inplace=True)
    df_no_nan = df[~(df['MP'].isna())&~(df['Salary'].isna())]
    return df_no_nan


if __name__ == '__main__':
    pass