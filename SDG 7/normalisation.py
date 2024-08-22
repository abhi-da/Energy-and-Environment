import numpy as np
import pandas as pd
import os

df=pd.read_csv(r'F:\GitHub\SDG\cleaned_afg.csv')
min_max_df=pd.read_csv(r'F:\GitHub\SDG\min_max_values.csv',index_col=0)

min_v = pd.to_numeric(min_max_df['min value'], errors='coerce')
max_v = pd.to_numeric(min_max_df['max value'], errors='coerce')

df_normalised=df.copy()


for column in df.columns:
    if column in min_v.index and column in max_v.index:
      min = min_v[column]
      max=max_v[column]
    
      if max != min:
        df_normalised[column] = (df[column] - min)*100 / (max - min)
      else:
        df_normalised[column] = 0

df_normalised.to_csv('normalised_afg.csv',index=False)

sdg=df_normalised['mean index']=df_normalised.mean(axis=1)
sdg.to_csv('sdg afg.csv',index=False)

#df_normalised.to_csv('normalised_data_afghanistan.csv', index=False)