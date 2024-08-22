import pandas as pd
import numpy as np
import os
import glob

input_directory = r'F:\GitHub\SDG\Country Data'
output_directory = r'F:\GitHub\SDG\Country_data_cleaned'

os.makedirs(output_directory, exist_ok=True)

csv_files = glob.glob(os.path.join(input_directory, '*.csv'))

min_value = 0
max_value = 100


for file_path in csv_files:
    
    df = pd.read_csv(file_path)
 
    
 
    first_column = df.columns[0]
    columns_to_interpolate = df.columns[1:]
    df[columns_to_interpolate] = df[columns_to_interpolate].interpolate(method='spline', order=1)
    df[columns_to_interpolate] = df[columns_to_interpolate].clip(lower=min_value, upper=max_value)

    output_file_path = os.path.join(output_directory, f'cleaned_{os.path.basename(file_path)}')
    df.to_csv(output_file_path, index=False)

    print(df[columns_to_interpolate])

