import enum
import os
import pandas as pd
from statistics import mean

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


class GunLawsColumnNames(enum.Enum):
    '''
    Represents column names in gun_laws_df.
    '''
    COUNTRY = 'Country',
    GOOD_REASON = 'Good Reason Required',
    PERSONAL_PROTECTION = 'Personal Protection Permitted',
    LONG_GUNS = 'Long Guns Permitted',
    HANDGUNS = 'Handguns Permitted',
    SEMIAUTOMATIC = 'Semi-Automatic Permitted',
    FULLY_AUTOMATIC = 'Fully Automatic Permitted',
    OPEN_CARRY = 'Open Carry Permitted',
    CONCEALED_CARRY = 'Concealed Carry Permitted',
    FREE_OF_REGISTRATION = 'Free of Registration'

# Drop unwanted columns and rename remaining.
gun_laws_df.drop(['Magazine capacity limits[N 1]', 'Max penalty (years)[2]'], axis=1, inplace=True)
gun_laws_df.rename(columns={
    'Region': GunLawsColumnNames.COUNTRY.value,
    'Good reason required?[3]': GunLawsColumnNames.GOOD_REASON.value,
    'Personal protection': GunLawsColumnNames.PERSONAL_PROTECTION.value,
    'Long guns (exc. semi- and full-auto)[4]': GunLawsColumnNames.LONG_GUNS.value,
    'Handguns[5]': GunLawsColumnNames.HANDGUNS.value,
    'Semi-automatic rifles': GunLawsColumnNames.SEMIAUTOMATIC.value,
    'Fully automatic firearms[6]': GunLawsColumnNames.FULLY_AUTOMATIC.value,
    'Open carry[7]': GunLawsColumnNames.OPEN_CARRY.value,
    'Concealed carry[8]': GunLawsColumnNames.CONCEALED_CARRY.value,
    'Free of registration[1]': GunLawsColumnNames.FREE_OF_REGISTRATION.value
}, inplace=True)

# Clean gun laws dataframe.
class Regulation(enum.Enum):
    NO_DATA = -1
    HIGHLY_REGULATED = 0
    MOSTLY_REGULATED = 1
    CONDITIONAL = 2
    MOSTLY_UNREGULATED = 3
    HIGHLY_UNREGULATED = 4

def get_regulation(cell: str, is_restriction: bool) -> Regulation:
    '''
    Given a cell from gun_laws_df and and a bool indicating whether or not this column 
    represents a restriction, returns a value from the Regulation enum.
    '''
    if not cell or pd.isna(cell) or cell.isspace() or cell.lower().strip() == 'n/a':
        return Regulation.NO_DATA

    lc_cell = cell.lower().strip()

    if 'total ban' in lc_cell:
        return Regulation.HIGHLY_REGULATED

    if lc_cell == 'no':
        return Regulation.HIGHLY_UNREGULATED if is_restriction else Regulation.HIGHLY_REGULATED

    if 'rarely issued' in lc_cell or 'rarely granted' in lc_cell:
        return Regulation.MOSTLY_REGULATED

    if lc_cell.startswith('no'):
        return Regulation.MOSTLY_UNREGULATED if is_restriction else Regulation.MOSTLY_REGULATED

    if lc_cell == 'yes':
        return Regulation.HIGHLY_REGULATED if is_restriction else Regulation.HIGHLY_UNREGULATED

    if lc_cell.startswith('yes') and 'shall issue' in lc_cell:
        return Regulation.HIGHLY_UNREGULATED

    if lc_cell.startswith('yes'):
        return Regulation.MOSTLY_REGULATED if is_restriction else Regulation.MOSTLY_UNREGULATED

    return Regulation.CONDITIONAL

def convert_to_regulations(row: pd.Series) -> None:
    '''
    Converts regulation-related cells in a given row from gun_laws_df to Regulation enum values.
    '''
    for column_name in GunLawsColumnNames:
        if column_name is GunLawsColumnNames.COUNTRY:
            continue
        is_restriction = column_name is GunLawsColumnNames.GOOD_REASON
        row[column_name.value] = get_regulation(row[column_name.value], is_restriction)

gun_laws_df.apply(convert_to_regulations, axis=1)

def calculate_mean_regulation(row: pd.Series):
    '''
    Calculates the mean regulation for row and appends as column.
    '''
    row['Summary Regulation'] = mean([row[column_name.value].value for column_name in GunLawsColumnNames 
        if column_name is not GunLawsColumnNames.COUNTRY and row[column_name.value] is not Regulation.NO_DATA])

gun_laws_df.apply(calculate_mean_regulation, axis=1)

print(gun_laws_df.head())