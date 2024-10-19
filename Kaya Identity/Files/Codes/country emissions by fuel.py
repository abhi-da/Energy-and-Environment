import pandas as pd
import matplotlib.pyplot as plt
import json

# Load the CO2 emissions data from JSON
with open('clean_Germany Emissions by Fuel.json', 'r') as file:
    data = json.load(file)



# Initialize an empty dictionary to hold the data for each sector
emissions_data = {'Year': []}

# Iterate over each sector in the JSON data
for sector in data:
    sector_name = sector['name']
    
    # Initialize a list to store the sector's emission values
    if sector_name not in emissions_data:
        emissions_data[sector_name] = []
    
    # Extract year and value from 'data' and append to emissions_data
    for entry in sector['data']:
        year = entry['date']
        value = entry['value']
        
        # Append year only once (assuming same years across sectors)
        if 'Year' not in emissions_data or year not in emissions_data['Year']:
            emissions_data['Year'].append(year)
        
        emissions_data[sector_name].append(value)

# Create a DataFrame from the emissions data
df = pd.DataFrame(emissions_data)

# Plot absolute values of CO2 emissions by sector
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each sector
for column in df.columns[1:]:  # Skipping the 'Year' column
    ax.plot(df['Year'], df[column], label=column, marker='o')

# Title and labels
ax.set_title('CO2 Emissions by Fuel (qbtu)', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('CO2 Emissions (qbtu)', fontsize=12)

# Ensure all years are shown on the x-axis
ax.set_xticks(df['Year'])  # Display all years
ax.set_xticklabels(df['Year'], rotation=45, ha='right')  # Rotate labels for readability
y_min = 0  # Adjust this based on the minimum CO2 value in your data
y_max = max(df.iloc[:, 1:].max())  # Get the maximum value across all columns
ax.set_yticks(range(y_min, int(y_max) + 50, 50))

# Customize grid lines
ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Place the legend below the chart
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='medium', ncol=2)

# Adjust the layout to make room for the legend
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save and show the plot
plt.savefig('CO2_Emissions_by_fuel.png', dpi=300, bbox_inches='tight')
plt.show()