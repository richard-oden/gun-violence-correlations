import os
import pandas as pd


def get_gun_deaths_df() -> pd.DataFrame:
    '''
    Imports Small-Arms-Survey-DB-violent-deaths.xlsx and parses as a dataframe.

    Returns
    ---
    a DataFrame object representing Small-Arms-Survey-DB-violent-deaths.xlsx
    '''
    return pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="D, AI", skiprows=[0, 1])

def get_gun_laws_df() -> pd.DataFrame:
    pass