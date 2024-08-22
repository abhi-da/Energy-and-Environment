import pandas as pd
import numpy as np
import os

output_folder = r'F:\GitHub\SDG\Country Data'

os.makedirs(output_folder, exist_ok=True)

file_path = r'F:\GitHub\SDG\sdg7.csv'
df = pd.read_csv(file_path)

unique_country=df['id'].unique()

for id in unique_country:
    country_data=df[df['id']==id]

    filename=os.path.join(output_folder, f'{id}_data.csv')

    country_data.to_csv(filename, index=False)

    print(f'saved {filename}')
