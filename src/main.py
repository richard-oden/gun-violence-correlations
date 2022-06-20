from bs4 import BeautifulSoup
import pandas as pd
import os
import requests

violent_deaths_df = pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="C, D, AI", skiprows=[0, 1])

gun_laws_request = requests.get('https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation')

if not gun_laws_request.ok:
    raise RuntimeError('Failed to retrieve gun laws wikipedia article.')

soup = BeautifulSoup(gun_laws_request.content, 'html.parser')
print(soup.prettify())