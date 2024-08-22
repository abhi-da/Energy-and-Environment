import pandas as pd
import numpy as np
import os
output_folder = r'F:\GitHub\SDG'
df=pd.read_csv(r'F:\GitHub\SDG\sdg7.csv')
dff=pd.read_csv(r'F:\GitHub\SDG\cleaned_afg.csv')


min_v=df.min()
max_v=df.max()

dff_normalized=dff.copy()

min_max_df=pd.DataFrame({
    'min value': min_v,
    'max value': max_v
})
min_max_df.to_csv('min_max_values.csv')
