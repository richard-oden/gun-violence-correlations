from bs4 import BeautifulSoup
import pandas as pd
import os
import requests

violent_deaths_df = pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="C, D, AI", skiprows=[0, 1])
gun_laws_df = pd.read_html('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation', match='Gun laws worldwide')[0]

gun_laws_df.columns = [col[1] for col in gun_laws_df.columns]

print(gun_laws_df[gun_laws_df['Region'].str.contains('Albania')])