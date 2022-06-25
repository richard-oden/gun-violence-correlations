import enum
import os
import pandas as pd
import re

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
gun_laws_df = gun_laws_df.droplevel(level=[0, 2], axis=1)

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

# Clean gun laws dataframe.
class Regulation(enum.Enum):
    NO_DATA = -1
    HIGHLY_REGULATED = 0
    MOSTLY_REGULATED = 1
    CONDITIONAL = 2
    MOSTLY_UNREGULATED = 3
    HIGHLY_UNREGULATED = 4

def get_regulation(desc: str, is_restriction: bool) -> int:
    '''
    Given a field from gun_laws_df and and a bool indicating whether or not this column 
    represents a restriction, returns a value from the Regulation enum.
    '''
    if not desc or desc.isspace() or desc.lower().strip() == 'n/a':
        return Regulation.NO_DATA

    lc_desc = desc.lower().strip()

    if 'total ban' in lc_desc:
        return Regulation.HIGHLY_REGULATED

    if lc_desc == 'no':
        return Regulation.HIGHLY_UNREGULATED if is_restriction else Regulation.HIGHLY_REGULATED

    if 'rarely issued' in lc_desc or 'rarely granted' in lc_desc:
        return Regulation.MOSTLY_REGULATED

    if lc_desc.startswith('no'):
        return Regulation.MOSTLY_UNREGULATED if is_restriction else Regulation.MOSTLY_REGULATED

    if lc_desc == 'yes':
        return Regulation.HIGHLY_REGULATED if is_restriction else Regulation.HIGHLY_UNREGULATED

    if lc_desc.startswith('yes') and 'shall issue' in lc_desc:
        return Regulation.HIGHLY_UNREGULATED

    if lc_desc.startswith('yes'):
        return Regulation.MOSTLY_REGULATED if is_restriction else Regulation.MOSTLY_UNREGULATED

    return Regulation.CONDITIONAL