import os
import re
import pandas as pd
import pycountry
import helpers.log_helper as lh
from enums.ColumnName import ColumnName, REGULATION_COLUMN_NAMES, TEXT_COLUMN_NAMES
from enums.Regulation import Regulation
from statistics import mean


def get_gun_deaths_df() -> pd.DataFrame:
    '''
    Imports Small-Arms-Survey-DB-violent-deaths.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing Small-Arms-Survey-DB-violent-deaths.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="C, D, AI", skiprows=[0, 1])


def clean_gun_deaths_df(gun_deaths_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Cleans the gun deaths dataframe.

    Parameters
    ---
    `gun_deaths_df` : `DataFrame` representing gun deaths by country

    Returns
    ---
    the cleaned `DataFrame` instance
    '''
    # Rename columns for readability.
    gun_deaths_df.rename(columns={
        'Unnamed: 2': ColumnName.COUNTRY_CODE.value,
        'Unnamed: 3': ColumnName.COUNTRY.value,
        'Rate.3': ColumnName.DEATH_RATE.value
    }, inplace=True)

    # Drop rows with no country.
    gun_deaths_df.dropna(subset=[ColumnName.COUNTRY_CODE.value, ColumnName.COUNTRY.value], inplace=True)

    return gun_deaths_df


def get_civilian_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Civilian-held-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Civilian-held-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Civilian-held-firearms-annexe.xlsx'), usecols="A, I", skiprows=[1, 2])


def clean_civilian_guns_df(civilian_guns_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Cleans the civilian guns dataframe.

    Parameters
    ---
    `gun_deaths_df` : `DataFrame` representing civilian gun holdings by country

    Returns
    ---
    the cleaned `DataFrame` instance
    '''
    # Drop unwanted rows/columns from dataframe.
    civilian_guns_df.dropna(inplace=True)

    # Rename columns for readability.
    civilian_guns_df.rename(columns={
        civilian_guns_df.columns[0]: ColumnName.COUNTRY_CODE.value,
        civilian_guns_df.columns[1]: ColumnName.CIVILIAN_FIREARMS.value
    }, inplace=True)

    # Convert civilian gun ownership rate to float and drop invalid values.
    civilian_guns_df[ColumnName.CIVILIAN_FIREARMS.value] = pd.to_numeric(civilian_guns_df[ColumnName.CIVILIAN_FIREARMS.value], errors='coerce')
    civilian_guns_df.dropna(inplace=True)

    return civilian_guns_df


def get_military_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Military-owned-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Military-owned-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Military-owned-firearms-annexe.xlsx'), usecols="A, E, I")


def clean_military_guns_df(military_guns_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Cleans the military guns dataframe.

    Parameters
    ---
    `gun_deaths_df` : `DataFrame` representing military gun holdings by country

    Returns
    ---
    the cleaned `DataFrame` instance
    '''
    # Drop unwanted rows/columns from dataframe.
    military_guns_df.dropna(inplace=True)

    # Convert population and firearm counts to int, then drop any invalid rows.
    military_guns_df['Population'] = pd.to_numeric(military_guns_df['Population'], errors='coerce')
    military_guns_df['Firearms in sub-'] = pd.to_numeric(military_guns_df['Firearms in sub-'], errors='coerce')
    military_guns_df.dropna(inplace=True)

    # Compute guns per 100 persons.
    military_guns_df[ColumnName.MILITARY_FIREARMS.value] = military_guns_df.apply(get_guns_per_100_persons, args=('Population', 'Firearms in sub-'), axis=1)

    # Drop columns used for calculation.
    military_guns_df.drop(['Population', 'Firearms in sub-'], axis=1, inplace=True)

    # Rename columns for readability.
    military_guns_df.rename(columns={
        'Country': ColumnName.COUNTRY_CODE.value
    }, inplace=True)

    return military_guns_df


def get_police_guns_df() -> pd.DataFrame:
    '''
    Imports SAS-BP-Law-enforcement-firearms-annexe.xlsx and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing SAS-BP-Law-enforcement-firearms-annexe.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'SAS-BP-Law-enforcement-firearms-annexe.xlsx'), usecols="A, E, H", skiprows=range(5))


def clean_police_guns_df(police_guns_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Cleans the police guns dataframe.

    Parameters
    ---
    `gun_deaths_df` : `DataFrame` representing law enforcement gun holdings by country

    Returns
    ---
    the cleaned `DataFrame` instance
    '''
    # Convert population and firearm counts to int, then drop any invalid rows.
    police_guns_df['Unnamed: 4'] = pd.to_numeric(police_guns_df['Unnamed: 4'], errors='coerce')
    police_guns_df['Unnamed: 7'] = pd.to_numeric(police_guns_df['Unnamed: 7'], errors='coerce')
    police_guns_df.dropna(inplace=True)

    # Compute guns per 100 persons.
    police_guns_df[ColumnName.POLICE_FIREARMS.value] = police_guns_df.apply(get_guns_per_100_persons, args=('Unnamed: 4', 'Unnamed: 7'), axis=1)

    # Drop columns used for calculation.
    police_guns_df.drop(['Unnamed: 4', 'Unnamed: 7'], axis=1, inplace=True)

    # Rename columns for readability.
    police_guns_df.rename(columns={
        'Unnamed: 0': ColumnName.COUNTRY_CODE.value
    }, inplace=True)

    return police_guns_df


def get_gun_laws_df() -> pd.DataFrame:
    '''
    Imports gun laws by nation table from wikipedia and parses as a `DataFrame`.

    Returns
    ---
    `DataFrame` object representing gun laws by nation table
    '''
    return pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]


def clean_gun_laws_df(gun_laws_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Cleans the gun laws dataframe.

    Parameters
    ---
    `gun_deaths_df` : `DataFrame` representing gun legislation by country

    Returns
    ---
    the cleaned `DataFrame` instance
    '''
    # Convert MultiIndex to single Index.
    gun_laws_df = gun_laws_df.droplevel(level=[0, 2], axis=1)

    # Drop unwanted columns and rename remaining.
    gun_laws_df.drop(['Magazine capacity limits[N 1]', 'Max penalty (years)[2]'], axis=1, inplace=True)
    gun_laws_df.rename(columns={
        'Region': ColumnName.COUNTRY.value,
        'Good reason required?[3]': ColumnName.GOOD_REASON_TEXT.value,
        'Personal protection': ColumnName.PERSONAL_PROTECTION_TEXT.value,
        'Long guns (exc. semi- and full-auto)[4]': ColumnName.LONG_GUNS_TEXT.value,
        'Handguns[5]': ColumnName.HANDGUNS_TEXT.value,
        'Semi-automatic rifles': ColumnName.SEMIAUTOMATIC_TEXT.value,
        'Fully automatic firearms[6]': ColumnName.FULLY_AUTOMATIC_TEXT.value,
        'Open carry[7]': ColumnName.OPEN_CARRY_TEXT.value,
        'Concealed carry[8]': ColumnName.CONCEALED_CARRY_TEXT.value,
        'Free of registration[1]': ColumnName.FREE_OF_REGISTRATION_TEXT.value
    }, inplace=True)

    # Drop rows that represent subheadings.
    gun_laws_df = gun_laws_df[gun_laws_df[ColumnName.COUNTRY.value] != 'Region']

    # Get country codes for gun laws dataframe.
    gun_laws_df[ColumnName.COUNTRY_CODE.value] = gun_laws_df.apply(get_country_code, axis=1)
    gun_laws_df.drop([ColumnName.COUNTRY.value], axis=1, inplace=True)

    # Drop rows where no country code was found.
    gun_laws_df.dropna(subset=[ColumnName.COUNTRY_CODE.value], inplace=True)

    # Add Regulation enum values to cells.
    convert_to_regulations(gun_laws_df)

    # Add overall regulation column to dataframe 
    gun_laws_df[ColumnName.OVERALL_REGULATION.value] = gun_laws_df.apply(get_mean_regulation, axis=1)

    return gun_laws_df


def get_country_code(row: pd.Series) -> str | None:
    '''
    Tries to find an alpha-3 code given `row.Country`.

    Parameters
    ---
    `row` : Series representing a row.

    Returns
    ---
    `str` representing alpha-3 country code, or `None` if no country is found.
    '''

    # remove anything in square brackets or parentheses before searching:
    try:
        query = re.sub(r'\[.*?\]', '', row[ColumnName.COUNTRY.value])
        query = re.sub(r'\(.*?\)', '', query)
        countries = pycountry.countries.search_fuzzy(query)
        
        if countries is None or len(countries) == 0:
            return

        return countries[0].alpha_3
    except LookupError:
        return


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
    Adds cells to the given `DataFrame` with `Regulation` enum values where applicable.

    Parameters
    ---
    `df` : `DataFrame` which will have its cell values converted to `Regulation` enum values
    '''
    for column_name in TEXT_COLUMN_NAMES:
        is_restriction = column_name is ColumnName.GOOD_REASON_TEXT
        index = TEXT_COLUMN_NAMES.index(column_name)
        df[REGULATION_COLUMN_NAMES[index].value] = df.apply(get_regulation, axis=1, args=(column_name.value, is_restriction))


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
    return (int(row[guns_col_name]) / int(row[population_col_name])) * 100


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
    gun_deaths_import_start = lh.start_timed_log('Importing gun deaths dataset.')
    gun_deaths_df = get_gun_deaths_df()
    lh.stop_timed_log('Finished importing gun deaths dataset.', gun_deaths_import_start)
    
    gun_deaths_cleaning_start = lh.start_timed_log('Cleaning gun deaths dataset.')
    gun_deaths_df = clean_gun_deaths_df(gun_deaths_df)
    lh.stop_timed_log('Finished cleaning gun deaths dataset.', gun_deaths_cleaning_start)

    # Create civilian gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Civilian-held-firearms-annexe.xlsx
    civilian_guns_import_start = lh.start_timed_log('Importing civilian guns dataset.')
    civilian_guns_df = get_civilian_guns_df()
    lh.stop_timed_log('Finished importing civilian guns dataset.', civilian_guns_import_start)

    civilian_guns_cleaning_start = lh.start_timed_log('Cleaning civilian guns dataset.')
    civilian_guns_df = clean_civilian_guns_df(civilian_guns_df)
    lh.stop_timed_log('Finished cleaning civilian guns dataset.', civilian_guns_cleaning_start)

    # Create military gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Military-owned-firearms-annexe.xlsx
    military_guns_import_start = lh.start_timed_log('Importing military guns dataset.')
    military_guns_df = get_military_guns_df()
    lh.stop_timed_log('Finished importing military guns dataset.', military_guns_import_start)
    
    military_guns_cleaning_start = lh.start_timed_log('Cleaning military guns dataset.')
    military_guns_df = clean_military_guns_df(military_guns_df)
    lh.stop_timed_log('Finished cleaning military guns dataset.', military_guns_cleaning_start)

    # Create police gun holdings dataframe from Small Arms Survey pdf.
    # https://www.smallarmssurvey.org/sites/default/files/resources/SAS-BP-Law-enforcement-firearms-annexe.xlsx
    police_guns_import_start = lh.start_timed_log('Importing police guns dataset.')
    police_guns_df = get_police_guns_df()
    lh.stop_timed_log('Finished importing police guns dataset.', police_guns_import_start)

    police_guns_cleaning_start = lh.start_timed_log('Cleaning police guns dataset.')
    police_guns_df = clean_police_guns_df(police_guns_df)
    lh.stop_timed_log('Finished cleaning police guns dataset.', police_guns_cleaning_start)

    # Create gun laws dataframe from wikipedia article.
    # https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation
    gun_laws_import_start = lh.start_timed_log('Importing gun laws dataset.')
    gun_laws_df = get_gun_laws_df()
    lh.stop_timed_log('Finished importing gun laws dataset.', gun_laws_import_start)
    
    gun_laws_cleaning_start = lh.start_timed_log('Cleaning gun laws dataset.')
    gun_laws_df = clean_gun_laws_df(gun_laws_df)
    lh.stop_timed_log('Finished cleaning gun laws dataset.', gun_laws_cleaning_start)

    # Merge dataframes, dropping rows that do not have a share a country name.
    merge_start = lh.start_timed_log('Merging datasets.')
    merged_df = pd.merge(gun_laws_df, gun_deaths_df, how='inner', on=ColumnName.COUNTRY_CODE.value)
    merged_df = pd.merge(merged_df, civilian_guns_df, how='left', on=ColumnName.COUNTRY_CODE.value)
    merged_df = pd.merge(merged_df, military_guns_df, how='left', on=ColumnName.COUNTRY_CODE.value)
    merged_df = pd.merge(merged_df, police_guns_df, how='left', on=ColumnName.COUNTRY_CODE.value)
    lh.stop_timed_log('Finished merging datasets.', merge_start)

    return merged_df