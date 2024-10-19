import pandas as pd
import json

# Step 1: Load JSON data into a DataFrame
json_file_path = 'pivoted_kaya.json'  # Replace with your actual JSON file path

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Create DataFrame from the JSON data
df_json = pd.DataFrame(json_data)

# Step 2: Calculate CO₂ emissions intensity
df_json['CO2 Intensity'] = df_json['CO2 emissions'] / df_json['Electricity net consumption']

# Step 3: Load CSV file into a DataFrame
csv_file_path = 'sdg7.2.csv'  # Replace with the path to your CSV file
df_csv = pd.read_csv(csv_file_path)

# Step 4: Extract 'n_sdg7_co2twh' column and rename it
sdg7_co2 = df_csv[['date', 'n_sdg7_co2twh']].rename(columns={'n_sdg7_co2twh': 'sdg7_co2'})

# Step 5: Merge both DataFrames based on the 'date' column
merged_df = pd.merge(df_json[['date', 'CO2 Intensity']], sdg7_co2, on='date', how='inner')

# Step 6: Calculate the difference
merged_df['Difference'] = merged_df['CO2 Intensity'] - merged_df['sdg7_co2']

# Step 7: Save the result to a new CSV file
output_file_path = 'output_differences.csv'  # Desired output file path
merged_df[['date', 'CO2 Intensity', 'sdg7_co2', 'Difference']].to_csv(output_file_path, index=False)

print("Processing completed. The results have been saved to:", output_file_path)
