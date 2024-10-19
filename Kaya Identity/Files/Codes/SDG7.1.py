import pandas as pd
import json

# Step 1: Load JSON data into a DataFrame
json_file_path = 'clean_Germany_Primary_Energy_Supply.json'  # Replace with your actual JSON file path

try:
    # Load JSON data from the file
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    exit()

# Convert JSON to a DataFrame
df_json = pd.DataFrame(json_data)

# Step 2: Extract relevant columns for total energy consumption and renewables
total_energy_consumption = df_json[df_json['name'] == "Total energy consumption"].iloc[0]['data']
renewable_energy_consumption = df_json[df_json['name'] == "Total energy consumption from renewables and other"].iloc[0]['data']

# Convert the extracted data into DataFrames
df_total = pd.DataFrame(total_energy_consumption)
df_renewable = pd.DataFrame(renewable_energy_consumption)

# Step 3: Calculate the ratio of total to renewable energy consumption
df_ratio = df_total.copy()
df_ratio['Renewable Ratio'] = (df_renewable['value'] / df_total['value'])*100

# Step 4: Load the SDG7.1 data from CSV
csv_file_path = 'sd7.1.csv'  # Replace with the path to your CSV file
try:
    df_sdg7_1 = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
    exit()

# Extract year and sdg7.1 column
sdg7_1 = df_sdg7_1[['date', 'sdg7_renewcon']]  # Adjust column names as necessary

# Step 5: Merge the ratio DataFrame with the SDG7.1 DataFrame
merged_df = pd.merge(df_ratio[['date', 'Renewable Ratio']], sdg7_1, on='date', how='inner')

# Step 6: Calculate the difference
merged_df['Difference'] = merged_df['Renewable Ratio'] - merged_df['sdg7_renewcon']

# Step 7: Save the result to a new CSV file
output_file_path = 'output_ratio_differences.csv'  # Desired output file path
merged_df[['date', 'Renewable Ratio', 'sdg7_renewcon', 'Difference']].to_csv(output_file_path, index=False)

print("Processing completed. The results have been saved to:", output_file_path)
