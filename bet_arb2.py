# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 09:55:36 2025

BETTING ARBITRAGE FOR 1 X 2
UPLOAD 3 EXCEL SHEETS WITH COLUMNS TIME, HOME, AWAY, 1, X, 2
GET THE BEST BEST COMBINATION FOR THE DAY

@author: LK
"""

import pandas as pd

stake = 100


csv_files = ['bet9ja_odds.csv', 'sportybet_odds.csv', '1xbet_odds.csv', 'msports_odds.csv']

dfs = [pd.read_csv(file) for file in csv_files]
prefixes = [file.replace('_odds.csv', '') for file in csv_files]


for i in range(len(dfs)):
    dfs[i] = dfs[i][['time', 'home', 'away', '1', 'X', '2']]
    dfs[i].columns = ['time', 'home', 'away', '1', 'X', '2']


# Function to extract the longest word from a given text
def get_longest_word(text):
    words = str(text).split()  # Split text into words
    if words:
        return max(words, key=len)  # Find the longest word
    return None

# Function to perform fuzzy lookup
def fuzzy_lookup(df_main, df_lookup, prefix):
    df_merged = df_main.copy()
    
    for i, row in df_main.iterrows():
        time_filter = df_lookup['time'] == row['time']
        home_match = df_lookup['home'].str.contains(get_longest_word(row['home']), case=False, na=False)  # Partial match
        away_match = df_lookup['away'].str.contains(get_longest_word(row['away']), case=False, na=False)  # Partial match

        match = df_lookup[time_filter & (home_match & away_match)]
        if not match.empty:
            df_merged.loc[i, f'{prefix}_1'] = match['1'].values[0]
            df_merged.loc[i, f'{prefix}_X'] = match['X'].values[0]
            df_merged.loc[i, f'{prefix}_2'] = match['2'].values[0]
        else:
            df_merged.loc[i, [f'{prefix}_1', f'{prefix}_X', f'{prefix}_2']] = [0, 0, 0]  # Fill missing values
    
    return df_merged


df_main = dfs[0] # Use columns from first df

for prefix, df_lookup in zip(prefixes, dfs):
    df_main = fuzzy_lookup(df_main, df_lookup, prefix)


df4 = df_main
# Rename df1 columns
# df4 = df4.rename(columns={'1': '1_1', 'X': '1_X', '2': '1_2'})

# Select and reorder columns
# df4 = df4[['time', 'home', 'away', '1_1', '1_X', '1_2', '2_1', '2_X', '2_2', '3_1', '3_X', '3_2']]

df4 = df4.dropna()
# Compute max value and its source column dynamically
for suffix in ['_1', '_X', '_2']:
    cols = [col for col in df4.columns if col.endswith(suffix) or col in ['_1', '_X', '_2']]
    
    # Find max value
    df4[f'H{suffix}'] = df4[cols].max(axis=1)
    
    # Find source column
    df4[f'Source{suffix}'] = df4[cols].idxmax(axis=1)

# Compute the inverse of H_1, H_X, and H_2
df4['inv_H_1'] = 1 / df4['H_1']
df4['inv_H_X'] = 1 / df4['H_X']
df4['inv_H_2'] = 1 / df4['H_2']

df4['sum_inv_H'] = df4[['inv_H_1', 'inv_H_X', 'inv_H_2']].sum(axis=1)

df4['bet_amt_1'] = df4['inv_H_1'] / df4['sum_inv_H'] * stake
df4['bet_amt_X'] = df4['inv_H_X'] / df4['sum_inv_H'] * stake
df4['bet_amt_2'] = df4['inv_H_2'] / df4['sum_inv_H'] * stake

df4['profit'] = ((df4['bet_amt_1'] * df4['H_1']) - stake)

print('Maximum profit: ', df4['profit'].max())

# Save Data to CSV
csv_filename = 'bet_arb.csv'
df4.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")


