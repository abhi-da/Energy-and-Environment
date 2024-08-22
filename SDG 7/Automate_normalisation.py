import pandas as pd
import numpy as np
import os
import glob

input_directory = r'F:\GitHub\Energy-and-Environment\SDG_afg\Country_data_cleaned'
output_directory = r'F:\GitHub\Energy-and-Environment\SDG_afg\sdg_index'

os.makedirs(output_directory, exist_ok=True)

csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
min_max_df = pd.read_csv(r'F:\GitHub\Energy-and-Environment\SDG_afg\min_max.csv', index_col=0)


min_v = pd.to_numeric(min_max_df['min value'], errors='coerce')
max_v = pd.to_numeric(min_max_df['max value'], errors='coerce')
print(min_v)
print(max_v)

for file_path in csv_files:
    df = pd.read_csv(file_path)
    df = df.iloc[:, 1:]
    


    df = df.apply(pd.to_numeric, errors='coerce')

    for column in df.columns:
        if column in min_v.index and column in max_v.index:
            min_val = min_v[column]
            max_val = max_v[column]

            if pd.notna(min_val) and pd.notna(max_val):  
                if max_val != min_val:
                    df[column] = (df[column] - min_val) * 100 / (max_val - min_val)
                    df[column] = df[column].clip(0, upper=100)
                else:
                    df[column] = 0
    
    sdg=df['mean index']=df.mean(axis=1)
    output_file_path = os.path.join(output_directory, f'sdg_index_{os.path.basename(file_path)}')
    sdg.to_csv(output_file_path,index=False)

    


