import pandas as pd
import json

# Load the cleaned primary energy supply data from JSON
country = 'World'  # Change country if needed
with open(f'/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_{country}_Primary_Energy_Supply.json', 'r') as file:
    data = json.load(file)

# Prepare the data for DataFrame
converted_data = []
for item in data:
    for entry in item['data']:
        year = entry['date']
        value = entry['value']
        if value != '--':  # Exclude invalid data points
            converted_data.append({"name": item['name'], 'year': year, 'value': float(value)})

# Create a DataFrame
df = pd.DataFrame(converted_data)

# Pivot the DataFrame
pivot_df = df.pivot_table(index='year', columns='name', values='value', aggfunc='first')
pivot_df.reset_index(inplace=True)

# Ensure the year column is treated as an integer
pivot_df['year'] = pivot_df['year'].astype(int)

# Normalize column names to lowercase
pivot_df.columns = pivot_df.columns.str.strip().str.lower()

# Set the correct names for total energy supply and coal consumption
total_energy_supply_col = 'total energy consumption'  # Adjust if needed
coal_consumption_col = 'total energy consumption from coal'  # Provided column name
exclude_share_col = 'total energy consumption from nuclear, renewables, and other'  # Column to exclude

# Exclude certain columns for share calculation
columns_excluded = ['year', total_energy_supply_col, exclude_share_col]

# Filter columns that are not in the excluded list
columns_sum = [col for col in pivot_df.columns if col not in columns_excluded]

# Calculate shares for each sector
share_columns = []  # Initialize the share_columns list
for col in columns_sum:
    share_col_name = col + ' share'
    pivot_df[share_col_name] = (pivot_df[col] / pivot_df[total_energy_supply_col]) * 100
    share_columns.append(share_col_name)  # Append the new share column name to the list

# Prepare results for peak and dip analysis
peak_dip_analysis = {}
peak_dip_share_analysis = {}

# Analyze peaks and dips for each sector
for col in columns_sum:
    # Find the year and value of the maximum
    max_value = pivot_df[col].max()
    max_year = pivot_df.loc[pivot_df[col] == max_value, 'year'].values[0]

    # Find the year and value of the minimum
    min_value = pivot_df[col].min()
    min_year = pivot_df.loc[pivot_df[col] == min_value, 'year'].values[0]

    peak_dip_analysis[col] = {
        'peak': {'year': max_year, 'value': max_value},
        'dip': {'year': min_year, 'value': min_value}
    }

# Analyze peaks and dips for each share sector
for col in share_columns:
    # Find the year and value of the maximum share
    max_share_value = pivot_df[col].max()
    max_share_year = pivot_df.loc[pivot_df[col] == max_share_value, 'year'].values[0]

    # Find the year and value of the minimum share
    min_share_value = pivot_df[col].min()
    min_share_year = pivot_df.loc[pivot_df[col] == min_share_value, 'year'].values[0]

    peak_dip_share_analysis[col] = {
        'peak': {'year': max_share_year, 'value': max_share_value},
        'dip': {'year': min_share_year, 'value': min_share_value}
    }

# Prepare the results for output
results = []

# Add peak/dip analysis to results
for sector, analysis in peak_dip_analysis.items():
    results.append(f"Sector: {sector}")
    results.append(f"  Peak: {analysis['peak']['year']} with a value of {analysis['peak']['value']:.2f}")
    results.append(f"  Dip: {analysis['dip']['year']} with a value of {analysis['dip']['value']:.2f}")
    results.append("")  # Blank line for readability

# Add share analysis to results
for sector, analysis in peak_dip_share_analysis.items():
    results.append(f"Share of {sector}:")
    results.append(f"  Peak: {analysis['peak']['year']} with a share of {analysis['peak']['value']:.2f}%")
    results.append(f"  Dip: {analysis['dip']['year']} with a share of {analysis['dip']['value']:.2f}%")
    results.append("")  # Blank line for readability

# Save results to a text file
with open('world_energy_supply_peak_dip_analysis.txt', 'w') as f:
    for line in results:
        f.write(line + '\n')

print("Peak and dip analysis results for both energy supply and shares have been saved to 'energy_supply_peak_dip_analysis.txt'")
