import pandas as pd
import os

# Create gun deaths dataframe from Small Arms Survey excel document.
# https://www.smallarmssurvey.org/database/global-violent-deaths-gvd
gun_deaths_df = pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="D, AI", skiprows=[0, 1])

# Rename columns for readability.
gun_deaths_df.rename(columns={
    'Unnamed: 3': 'Country',
    'Rate.3': 'Violent deaths by firearm'
}, inplace=True)

# Create gun laws dataframe from wikipedia article.
gun_laws_df = pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]

# Convert MultiIndex to single Index.
gun_laws_df.columns = [col[1] for col in gun_laws_df.columns]

# Drop unwanted columns and rename remaining.
gun_laws_df.drop(['Magazine capacity limits[N 1]', 'Max penalty (years)[2]'], axis=1, inplace=True)
gun_laws_df.rename(columns={
    'Region': 'Country',
    'Good reason required?[3]': 'Good reason required',
    'Personal protection': 'Personal protection permitted',
    'Long guns (exc. semi- and full-auto)[4]': 'Long guns permitted',
    'Handguns[5]': 'Handguns permitted',
    'Semi-automatic rifles': 'Semi-automatic permitted',
    'Fully automatic firearms[6]': 'Fully automatic permitted',
    'Open carry[7]': 'Open carry permitted',
    'Concealed carry[8]': 'Concealed carry permitted',
    'Free of registration[1]': 'Free of registration'
}, inplace=True)

print(gun_laws_df.columns)