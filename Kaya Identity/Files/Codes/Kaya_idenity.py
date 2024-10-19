import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import CubicSpline
from scipy.interpolate import make_interp_spline
from sklearn.preprocessing import MinMaxScaler

# Load the datasets from JSON files
with open('clean_Germany_Electricity_Consumption.json') as f:
    E = json.load(f)
with open('clean_Germany_GDP.json') as f:
    G = json.load(f)
with open('clean_Germany_Population.json') as f:
    P = json.load(f)
with open('clean_Germany Emissions by Fuel.json') as f:
    F = json.load(f)

sectors_to_extract = {
    'clean_Germany_Electricity_Consumption.json': 'Electricity net consumption',  
    'clean_Germany_GDP.json': 'GDP at purchasing power parities',   
    'clean_Germany_Population.json': 'Population',                   
    'clean_Germany Emissions by Fuel.json': 'CO2 emissions'  
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

# Extract data for the specified sectors from all four files
merged_data = []  

for file, sector_name in sectors_to_extract.items():
    sector_data = None
    if file == 'clean_Germany_Electricity_Consumption.json':
        sector_data = extract_sector_data(E, sector_name)
    elif file == 'clean_Germany_GDP.json':
        sector_data = extract_sector_data(G, sector_name)
    elif file == 'clean_Germany_Population.json':
        sector_data = extract_sector_data(P, sector_name)
    elif file == 'clean_Germany Emissions by Fuel.json':
        sector_data = extract_sector_data(F, sector_name)

    if sector_data:  
        for entry in sector_data['data']:
            entry['sector'] = sector_data['name']
            merged_data.append(entry)

# Save the merged data to a single JSON file
with open('merged_data.json', 'w') as json_file:
    json.dump(merged_data, json_file, indent=4)

# Convert the merged data to a DataFrame
df = pd.DataFrame(merged_data)
print(df)
pivoted_df = df.pivot(index='date', columns='sector', values='value').reset_index()

# Save the DataFrame to a CSV file
df.to_csv('merged_data.csv', index=False)

print("Data saved to 'merged_data.json' and 'merged_data.csv'.")

# Save the merged data to a single CSV file
pivoted_df.to_csv('kaya.csv', index=False)
with open('Kaya.json', 'w') as json_file:
    json.dump(merged_data, json_file, indent=4)
pivoted_df.to_json('pivoted_kaya.json', orient='records', indent=4)

print("Data saved to 'merged_data.csv'.")
print(pivoted_df.columns)

# Calculate additional metrics
pivoted_df['GDP per capita'] = pivoted_df['GDP at purchasing power parities'] / pivoted_df['Population']
pivoted_df['Energy intensity'] = pivoted_df['Electricity net consumption'] / pivoted_df['GDP at purchasing power parities']
pivoted_df['Carbon intensity'] = pivoted_df['CO2 emissions'] / pivoted_df['Electricity net consumption']

# Rename 'CO2 emissions' to 'Emissions (F)' for clarity
pivoted_df.rename(columns={'CO2 emissions': 'Emissions (F)'}, inplace=True)
intensive_df = pivoted_df[['date', 'Population', 'GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)']]

# Display the first few rows of the DataFrame with the new columns
print(pivoted_df[['date','Population', 'GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)']].head())
print(intensive_df.columns)



# def normalize(series):
#     return (series - series.min()) / (series.max() - series.min())

# # Plot normalized values of the different sectors with smooth trend lines
# fig, ax = plt.subplots(figsize=(12, 8))

# # Define the columns for plotting
# columns_to_plot = ['GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)', 'Population']

# # Normalize and plot each column with smoothing
# for column in columns_to_plot:
#     sector_data = intensive_df[['date', column]].dropna().copy()  # Avoid NaNs and copy relevant data
    
#     # Normalize the column data
#     sector_data['normalized_value'] = normalize(sector_data[column])
    
#     # Smooth the trend line using make_interp_spline
#     x = np.array(sector_data['date'])
#     y = np.array(sector_data['normalized_value'])
    
#     # Create a new set of x values for smoothing
#     x_smooth = np.linspace(x.min(), x.max(), 30)  # Increase resolution
#     spline = make_interp_spline(x, y, k=3)  # k=3 for cubic spline
#     y_smooth = spline(x_smooth)
    
#     # Plot the smoothed values with thinner lines and smaller markers
#     ax.plot(x_smooth, y_smooth, label=column, linewidth=1.5, markersize=4, marker='o', alpha=0.8)

# # Title and labels
# ax.set_title('Factors in Kaya Identity (Smoothened)', fontsize=14, fontweight='bold')
# ax.set_xlabel('Year', fontsize=12)
# ax.set_ylabel('Normalized Values (0 to 1)', fontsize=12)

# # Ensure all years are shown on the x-axis
# ax.set_xticks(intensive_df['date'].unique())  # Use unique dates for the x-axis
# ax.set_xticklabels(intensive_df['date'].unique(), rotation=45, ha='right')

# # Customize grid lines
# ax.grid(True, which='both', linestyle='--', linewidth=0.2, alpha=0.5)

# # Place the legend below the chart
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='medium', ncol=2)

# # Adjust the layout to make room for the legend
# plt.tight_layout(rect=[0, 0, 1, 0.95])

# # Save and show the plot
# plt.savefig('Kaya_smooth_intensive.png', dpi=300, bbox_inches='tight')
# plt.show()





# Calculate growth rates
# Calculate growth rates
growth_rate_df = intensive_df.copy()
variables = ['Population', 'GDP per capita', 'Energy intensity', 'Carbon intensity', 'Emissions (F)']

# Calculate growth rates
for var in variables:
    growth_rate_df[f'{var} Growth Rate (%)'] = (growth_rate_df[var].diff() / growth_rate_df[var].shift(1)) * 100

# Dropping rows with NaN values that result from the diff() operation
growth_rate_df.dropna(inplace=True)

# Saving to CSV
growth_rate_df.to_csv('growth_rates_kaya_intensive.csv', index=False)

# Saving to JSON
growth_rate_df.to_json('growth_rates_kaya_intensive.json', orient='records', lines=True)

# Save only the newly created growth rate variables
growth_rate_only_df = growth_rate_df[['date'] + [f'{var} Growth Rate (%)' for var in variables]]

# Calculate the sum of the specified growth rates and add it as a new column
growth_rate_columns = [
    'Population Growth Rate (%)',
    'Carbon intensity Growth Rate (%)',
    'GDP per capita Growth Rate (%)',
    'Energy intensity Growth Rate (%)'
]

# Calculate the sum of the specified growth rates and add it as a new column
growth_rate_only_df['emissions_new(F)'] = growth_rate_only_df[growth_rate_columns].sum(axis=1)

# Calculate the growth rate for 'Emissions (F)' and store it in growth_rate_only_df
growth_rate_only_df['Emissions (F) Growth Rate (%)'] = growth_rate_df['Emissions (F) Growth Rate (%)']

# Calculate the difference between 'emissions_new(F)' and 'Emissions (F) Growth Rate (%)'
growth_rate_only_df['Difference (emissions_new(F) - Emissions (F) Growth Rate)'] = (
    growth_rate_only_df['emissions_new(F)'] - growth_rate_only_df['Emissions (F) Growth Rate (%)']
)

# Saving the updated growth rate only DataFrame to CSV and JSON
growth_rate_only_df.to_csv('growth_rate_only_kaya_intensive.csv', index=False)
growth_rate_only_df.to_json('growth_rate_only_kaya_intensive.json', orient='records', lines=True)

print("Growth rates calculated, differences added, and saved to CSV and JSON files.")
