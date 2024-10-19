
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, make_interp_spline
from sklearn.preprocessing import MinMaxScaler

# Load the datasets from JSON files
with open('/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_Germany_Primary_Energy_Supply.json') as f:
    E = json.load(f)
with open('/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_GDP.json') as f:
    G = json.load(f)
with open('/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_Population.json') as f:
    P = json.load(f)
with open('/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany Emissions by Fuel.json') as f:
    F = json.load(f)

# Sectors to extract
sectors_to_extract = {
    '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_Germany_Primary_Energy_Supply.json': 'Total energy consumption',  
    '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_GDP.json': 'GDP at purchasing power parities',   
    '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_Population.json': 'Population',                   
    '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_Emissions_by_Fuel.json': 'CO2 emissions'
}

# Function to extract data for the specified sector
def extract_sector_data(data, sector_name):
    for sector in data:
        if sector["name"] == sector_name:
            return {
                "name": sector["name"],
                "data": sector["data"]
            }
    return None  

# Extract data for the specified sectors from all files
merged_data = []  

for file, sector_name in sectors_to_extract.items():
    if file == '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_Germany_Primary_Energy_Supply.json':
        sector_data = extract_sector_data(E, sector_name)
    elif file == '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_GDP.json':
        sector_data = extract_sector_data(G, sector_name)
    elif file == '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_Population.json':
        sector_data = extract_sector_data(P, sector_name)
    elif file == '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 2/clean_Germany_Emissions_by_Fuel.json':
        sector_data = extract_sector_data(F, sector_name)

    if sector_data:  
        for entry in sector_data['data']:
            entry['sector'] = sector_data['name']
            merged_data.append(entry)

# Save the merged data to JSON and CSV
with open('merged_data_new.json', 'w') as json_file:
    json.dump(merged_data, json_file, indent=4)

df = pd.DataFrame(merged_data)
df.to_csv('merged_data_new.csv', index=False)

# Pivot the DataFrame
pivoted_df = df.pivot(index='date', columns='sector', values='value').reset_index()
pivoted_df.to_csv('kaya_new.csv', index=False)
pivoted_df.to_json('pivoted_kaya_new.json', orient='records', indent=4)

# Calculate additional metrics
pivoted_df['GDP per capita'] = pivoted_df['GDP at purchasing power parities'] / pivoted_df['Population']
pivoted_df['Energy intensity'] = pivoted_df['Total energy consumption'] / pivoted_df['GDP at purchasing power parities']
pivoted_df['Carbon intensity'] = pivoted_df['CO2 emissions'] / pivoted_df['Total energy consumption']

# Rename 'CO2 emissions' to 'Emissions (F)' for clarity
pivoted_df.rename(columns={'CO2 emissions': 'Emissions (F)'}, inplace=True)
intensive_df = pivoted_df[['date', 'Population', 'GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)']]

# Plot normalized values with trend lines
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

fig, ax = plt.subplots(figsize=(12, 8))
columns_to_plot = ['GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)', 'Population']

for column in columns_to_plot:
    sector_data = intensive_df[['date', column]].dropna().copy()
    sector_data['normalized_value'] = normalize(sector_data[column])
    x = np.array(sector_data['date'])
    y = np.array(sector_data['normalized_value'])
    x_smooth = np.linspace(x.min(), x.max(), 30)
    spline = make_interp_spline(x, y, k=3)
    y_smooth = spline(x_smooth)
    ax.plot(x_smooth, y_smooth, label=column, linewidth=1.5, markersize=4, marker='o', alpha=0.8)

ax.set_title('Factors in Kaya Identity (Smoothened)', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Normalized Values (0 to 1)', fontsize=12)
ax.set_xticks(intensive_df['date'].unique())
ax.set_xticklabels(intensive_df['date'].unique(), rotation=45, ha='right')
ax.grid(True, which='both', linestyle='--', linewidth=0.2, alpha=0.5)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='medium', ncol=2)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('Kaya_smooth_intensive_new.png', dpi=300, bbox_inches='tight')
plt.show()

# Growth rate calculations and difference checks
growth_rate_df = intensive_df.copy()
variables = ['Population', 'GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)']

for var in variables:
    growth_rate_df[f'{var} Growth Rate (%)'] = (growth_rate_df[var].diff() / growth_rate_df[var].shift(1)) * 100

growth_rate_df.dropna(inplace=True)
growth_rate_df.to_csv('growth_rates_kaya_intensive_new.csv', index=False)
growth_rate_df.to_json('growth_rates_kaya_intensive_new.json', orient='records', lines=True)

growth_rate_only_df = growth_rate_df[['date'] + [f'{var} Growth Rate (%)' for var in variables]]
growth_rate_columns = ['Population Growth Rate (%)', 'Carbon intensity Growth Rate (%)', 'GDP per capita Growth Rate (%)', 'Energy intensity Growth Rate (%)']

growth_rate_only_df['emissions_new(F)'] = growth_rate_only_df[growth_rate_columns].sum(axis=1)
growth_rate_only_df['Emissions (F) Growth Rate (%)'] = growth_rate_df['Emissions (F) Growth Rate (%)']
growth_rate_only_df['Difference (emissions_new(F) - Emissions (F) Growth Rate)'] = growth_rate_only_df['emissions_new(F)'] - growth_rate_only_df['Emissions (F) Growth Rate (%)']

growth_rate_only_df.to_csv('growth_rate_only_kaya_intensive_new.csv', index=False)
growth_rate_only_df.to_json('growth_rate_only_kaya_intensive_new.json', orient='records', lines=True)

print("Growth rates calculated, differences added, and saved to CSV and JSON files.")
