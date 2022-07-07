import os
import pandas as pd
import tabula
from enums.ColumnName import ColumnName, REGULATION_COLUMN_NAMES
from enums.Regulation import Regulation
from statistics import mean


def get_gun_deaths_df() -> pd.DataFrame:
    '''
    Imports Small-Arms-Survey-DB-violent-deaths.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing Small-Arms-Survey-DB-violent-deaths.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="D, AI", skiprows=[0, 1])


def get_civilian_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Civilian-held-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Civilian-held-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Civilian-held-firearms-annexe.xlsx'), usecols="B, I", skiprows=[1, 2])


def get_military_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Military-owned-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Military-owned-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Military-owned-firearms-annexe.xlsx'))


def get_police_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Law-enforcement-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Law-enforcement-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Law-enforcement-firearms-annexe.xlsx'))


def get_gun_laws_df() -> pd.DataFrame:
    '''
    Imports gun laws by nation table from wikipedia and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing gun laws by nation table
    '''
    return pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]


def get_country_name(gun_laws_row: pd.Series, gun_deaths_df: pd.DataFrame) -> str | None:
    '''
    If the Country in gun_laws_row is represented in gun_deaths_df, returns the value of the Country cell
    from from gun_deaths_df. Otherwise returns None.

    Parameters
    ---
    `gun_laws_row` : Series representing a row from gun_laws_df.
    `gun_deaths_df` : DataFrame of gun deaths by country.

    Returns
    ---
    `str` representing the value of the Country cell from `gun_deaths_df`, or `None` if no country is found.
    '''
    return next((country_name for country_name in gun_deaths_df[ColumnName.COUNTRY.value].tolist() 
        if country_name.lower().strip() in gun_laws_row[ColumnName.COUNTRY.value].lower()), None)


def get_regulation(row: pd.Series, column_name: str, is_restriction: bool) -> Regulation:
    '''
    Given a row, column name, and a bool indicating whether or not this column represents a restriction, 
    returns a value from the `Regulation` enum.

    Parameters
    ---
    `row` : `Series` representing a row from a `DataFrame`
    `column_name` : `str` name of the column to examine within `row`
    `is_restriction` : `bool` indicating whether or not this column represents a restriction

    Returns
    ---
    `Regulation` enum value
    '''

    cell = row[column_name]

    if not cell or pd.isna(cell) or cell.isspace() or cell.lower().strip() == 'n/a':
        return Regulation.NO_DATA.value

    lc_cell = cell.lower().strip()

    if 'total ban' in lc_cell:
        return Regulation.HIGHLY_REGULATED.value

    if lc_cell == 'no':
        return Regulation.HIGHLY_UNREGULATED.value if is_restriction else Regulation.HIGHLY_REGULATED.value

    if 'rarely issued' in lc_cell or 'rarely granted' in lc_cell:
        return Regulation.MOSTLY_REGULATED.value

    if lc_cell.startswith('no'):
        return Regulation.MOSTLY_UNREGULATED.value if is_restriction else Regulation.MOSTLY_REGULATED.value

    if lc_cell == 'yes':
        return Regulation.HIGHLY_REGULATED.value if is_restriction else Regulation.HIGHLY_UNREGULATED.value

    if lc_cell.startswith('yes') and 'shall issue' in lc_cell:
        return Regulation.HIGHLY_UNREGULATED.value

    if lc_cell.startswith('yes'):
        return Regulation.MOSTLY_REGULATED.value if is_restriction else Regulation.MOSTLY_UNREGULATED.value

    return Regulation.CONDITIONAL.value


def convert_to_regulations(df: pd.DataFrame) -> None:
    '''
    Modifies the cells in the given `DataFrame` to `Regulation` enum values where applicable.

    Parameters
    ---
    `df` : `DataFrame` which will have its cell values converted to `Regulation` enum values
    '''
    for column_name in REGULATION_COLUMN_NAMES:
        is_restriction = column_name is ColumnName.GOOD_REASON
        df[column_name.value] = df.apply(get_regulation, axis=1, args=(column_name.value, is_restriction))


def get_mean_regulation(row: pd.Series) -> float:
    '''
    Calculates the mean regulation for row.

    Parameters
    ---
    `row` : `Series` representing a row from a `DataFrame` object

    Returns
    ---
    `float` representing the mean `Regulation` of the row.
    '''
    return mean([row[column_name.value] for column_name in REGULATION_COLUMN_NAMES 
        if row[column_name.value] > Regulation.NO_DATA.value])


def get_guns_per_100_persons(row: pd.Series, population_col_name: str, guns_col_name: str) -> float:
    return (int(row[guns_col_name].replace(',', '')) / int(row[population_col_name].replace(',', ''))) * 100


def get_cleaned_data() -> pd.DataFrame:
    '''
    Retrieves and cleans data regarding gun legislation, gun ownership, and gun-releated deaths and returns 
    the result as a `DataFrame`.

    Returns
    ---
    `DataFrame` representing gun legislation and gun-related death data by country.
    '''
    # Create gun deaths dataframe from Small Arms Survey excel document.
    # https://www.smallarmssurvey.org/database/global-violent-deaths-gvd
    gun_deaths_df = get_gun_deaths_df()
    
    # Rename columns for readability.
    gun_deaths_df.rename(columns={
        'Unnamed: 3': ColumnName.COUNTRY.value,
        'Rate.3': ColumnName.DEATH_RATE.value
    }, inplace=True)

    # Drop rows with no country.
    gun_deaths_df.dropna(subset=[ColumnName.COUNTRY.value], inplace=True)

    # Create civilian gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Civilian-held-firearms-annexe.xlsx
    civilian_guns_df = get_civilian_guns_df()

    # Drop unwanted rows/columns from dataframe.
    civilian_guns_df.dropna(inplace=True)

    print(civilian_guns_df)

    # Rename columns for readability.
    civilian_guns_df.rename(columns={
        civilian_guns_df.columns[0]: ColumnName.COUNTRY.value,
        civilian_guns_df.columns[1]: ColumnName.CIVILIAN_FIREARMS.value
    }, inplace=True)

    print(civilian_guns_df)

    # Create military gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Military-owned-firearms-annexe.xlsx
    military_guns_df = get_military_guns_df()
    
    # Drop unwanted rows/columns from dataframe.
    military_guns_df.drop(range(3), inplace=True)
    military_guns_df = military_guns_df.loc[:, military_guns_df.columns.isin(['Country.1', 'Population', 'Total military'])]
    military_guns_df.dropna(inplace=True)

    # Compute guns per 100 persons.
    military_guns_df[ColumnName.MILITARY_FIREARMS.value] = military_guns_df.apply(get_guns_per_100_persons, args=('Population', 'Total military'), axis=1)

    # Drop columns used for calculation.
    military_guns_df.drop(['Total military', 'Population'], axis=1, inplace=True)

    # Rename columns for readability.
    military_guns_df.rename(columns={
        'Country.1': ColumnName.COUNTRY.value,
    }, inplace=True)

    # Create police gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Law-enforcement-firearms-annexe.xlsx
    police_guns_df = get_police_guns_df()

    # Create gun laws dataframe from wikipedia article.
    # https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation
    gun_laws_df = get_gun_laws_df()
    
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

    # Rename countries in gun laws dataframe so that they match countries in gun deaths dataframe.
    gun_laws_df[ColumnName.COUNTRY.value] = gun_laws_df.apply(get_country_name, axis=1, args=[gun_deaths_df])

    # Merge dataframes, dropping rows that do not have a share a country name.
    merged_df = pd.merge(gun_deaths_df, gun_laws_df, how='inner', on=ColumnName.COUNTRY.value)
    merged_df = pd.merge(merged_df, civilian_guns_df, how='inner', on=ColumnName.COUNTRY.value)

    print(merged_df)

    # Convert applicable cells in merged dataframe to Regulation enum values.
    convert_to_regulations(merged_df)

    # Add overall regulation column to merged dataframe 
    merged_df[ColumnName.OVERALL_REGULATION.value] = merged_df.apply(get_mean_regulation, axis=1)

    return merged_df