import pandas as pd
import os

df = pd.read_excel(os.path.join('data', 'Small-Arms-Survey-DB-violent-deaths.xlsx'), usecols="C, D, AI", skiprows=[0, 1])

print(df.head())