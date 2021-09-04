import pandas as pd 

def preprocessors(df,regions_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(regions_df, on='NOC', how='inner')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
