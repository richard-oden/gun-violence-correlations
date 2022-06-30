import os
import pandas as pd
from enums.ColumnName import ColumnName, REGULATION_COLUMN_NAMES
from enums.Regulation import Regulation


def get_gun_deaths_df() -> pd.DataFrame:
    '''
    Imports Small-Arms-Survey-DB-violent-deaths.xlsx and parses as a dataframe.

    Returns
    ---
    DataFrame object representing Small-Arms-Survey-DB-violent-deaths.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="D, AI", skiprows=[0, 1])

def get_gun_laws_df() -> pd.DataFrame:
    '''
    Imports gun laws by nation table from wikipedia and parses as a dataframe.

    Returns
    ---
    DataFrame object representing gun laws by nation table
    '''
    return pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]

def get_country_name(gun_laws_row: pd.Series, gun_deaths_df: pd.DataFrame) -> str | None:
    '''
    If the Country in gun_laws_row is represented in gun_deaths_df, returns the value of the Country cell
    from from gun_deaths_df. Otherwise returns None.

    Parameters
    ---
    gun_laws_row : Series representing a row from gun_laws_df.
    gun_deaths_df : DataFrame of gun deaths by country.

    Returns
    ---
    str representing the value of the Country cell from gun_deaths_df, or None if no country is found.
    '''
    return next((country_name for country_name in gun_deaths_df[ColumnName.COUNTRY.value].tolist() 
        if country_name.lower().strip() in gun_laws_row[ColumnName.COUNTRY.value].lower()), None)

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