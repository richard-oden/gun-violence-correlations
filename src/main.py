import os
import pandas as pd
from statistics import mean
from enums.Regulation import Regulation
from enums.ColumnName import ColumnName, REGULATION_COLUMN_NAMES

# Create gun deaths dataframe from Small Arms Survey excel document.
# https://www.smallarmssurvey.org/database/global-violent-deaths-gvd
gun_deaths_df = pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="D, AI", skiprows=[0, 1])

# Rename columns for readability.
gun_deaths_df.rename(columns={
    'Unnamed: 3': ColumnName.COUNTRY.value,
    'Rate.3': ColumnName.DEATH_RATE.value
}, inplace=True)

# Drop rows with no country.
gun_deaths_df.dropna(subset=[ColumnName.COUNTRY.value], inplace=True)

# Create gun laws dataframe from wikipedia article.
gun_laws_df = pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]

# Convert MultiIndex to single Index.
gun_laws_df = gun_laws_df.droplevel(level=[0, 2], axis=1)

# Drop unwanted columns and rename remaining.
gun_laws_df.drop(['Magazine capacity limits[N 1]', 'Max penalty (years)[2]'], axis=1, inplace=True)
gun_laws_df.rename(columns={
    'Region': ColumnName.COUNTRY.value,
    'Good reason required?[3]': ColumnName.GOOD_REASON.value,
    'Personal protection': ColumnName.PERSONAL_PROTECTION.value,
    'Long guns (exc. semi- and full-auto)[4]': ColumnName.LONG_GUNS.value,
    'Handguns[5]': ColumnName.HANDGUNS.value,
    'Semi-automatic rifles': ColumnName.SEMIAUTOMATIC.value,
    'Fully automatic firearms[6]': ColumnName.FULLY_AUTOMATIC.value,
    'Open carry[7]': ColumnName.OPEN_CARRY.value,
    'Concealed carry[8]': ColumnName.CONCEALED_CARRY.value,
    'Free of registration[1]': ColumnName.FREE_OF_REGISTRATION.value
}, inplace=True)

# Drop rows that represent subheadings.
gun_laws_df = gun_laws_df[gun_laws_df[ColumnName.COUNTRY.value] != 'Region']

# Clean gun laws dataframe.
def get_country_name(gun_laws_row: pd.Series) -> str | None:
    '''
    If the Country in gun_laws_row is represented in gun_deaths_df, returns the value of the Country cell
    from from gun_deaths_df. Otherwise returns None.
    '''
    return next((country_name for country_name in gun_deaths_df[ColumnName.COUNTRY.value].tolist() 
        if country_name.lower().strip() in gun_laws_row[ColumnName.COUNTRY.value].lower()), None)

gun_laws_df[ColumnName.COUNTRY.value] = gun_laws_df.apply(get_country_name, axis=1)

merged_df = pd.merge(gun_deaths_df, gun_laws_df, how='inner', on=ColumnName.COUNTRY.value)

def get_regulation(row: pd.Series, column_name: str, is_restriction: bool) -> Regulation:
    '''
    Given a row, column name, and a bool indicating whether or not this column represents a restriction, 
    returns a value from the Regulation enum.
    '''

    cell = row[column_name]

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

def convert_to_regulations(df: pd.DataFrame) -> None:
    '''
    Converts the cells in the given data frame to Regulation enum values where applicable.
    '''
    for column_name in REGULATION_COLUMN_NAMES:
        is_restriction = column_name is ColumnName.GOOD_REASON
        df[column_name.value] = df.apply(get_regulation, axis=1, args=(column_name.value, is_restriction))

convert_to_regulations(merged_df)

def get_mean_regulation(row: pd.Series) -> float:
    '''
    Calculates the mean regulation for row.
    '''
    return mean([row[column_name.value].value for column_name in REGULATION_COLUMN_NAMES 
        if row[column_name.value] is not Regulation.NO_DATA])

merged_df[ColumnName.OVERALL_REGULATION.value] = merged_df.apply(get_mean_regulation, axis=1)

print(merged_df)