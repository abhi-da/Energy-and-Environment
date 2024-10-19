import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Define paths for input JSON files and output files
world_file_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_World_Primary_Energy_Supply.json'  # Replace with your actual path
germany_file_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/clean_Germany_Primary_Energy_Supply.json'  # Replace with your actual path
output_csv_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/germany_world_primary_supply_share.csv'  # Path for the output CSV file
output_json_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/germany_world_primary_supply_share.json'  # Path for the output JSON file
plot_image_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/germany_world_primary_supply_share_plot.png'  # Path for the plot image

# Step 1: Load the JSON data
with open(world_file_path, 'r') as file:
    world_data = json.load(file)

with open(germany_file_path, 'r') as file:
    germany_data = json.load(file)

# Step 2: Calculate the share of Germany compared to the world
share_data = []

for germany_entry, world_entry in zip(germany_data, world_data):
    sector_name = germany_entry['name']
    
    for g_data, w_data in zip(germany_entry['data'], world_entry['data']):
        g_value = g_data['value']
        w_value = w_data['value']

        # Directly use the year from the data
        year = g_data['date']  # Assuming this is already the year

        # Ignore data before 1991, when Germany data starts
        if year and year >= 1991:
            # Only calculate the share if both values are valid and the World value is > 0
            if isinstance(g_value, (int, float)) and isinstance(w_value, (int, float)) and w_value > 0:
                if g_value <= w_value:
                    share = (g_value / w_value) * 100
                else:
                    share = None  # Germany's value should not be larger than World
            else:
                share = None  # Handle non-numeric or invalid cases

            # Append to the share data list
            share_data.append({
                'sector': sector_name,
                'year': year,
                'share': share
            })

# Step 3: Create a DataFrame
df = pd.DataFrame(share_data)

# Save the DataFrame to CSV and JSON files
df.to_csv(output_csv_path, index=False)
df.to_json(output_json_path, orient='records', lines=True)

print(f"Germany primary energy supply share data saved to '{output_csv_path}' and '{output_json_path}'")

# Step 4: Plot the shares with trend lines
plt.figure(figsize=(24, 12))

# Plotting each sector with a trend line and custom legend names
for sector in df['sector'].unique():
    sector_data = df[df['sector'] == sector]
    
    x = sector_data['year']
    y = sector_data['share']
    
    # Handle NaN values
    mask = ~y.isna()
    x = x[mask]
    y = y[mask]
    
    # Only apply smoothing if there are enough data points
    if len(x) >= 3:
        x_new = np.linspace(x.min(), x.max(), 300)  # 300 points for a smooth curve
        spline = make_interp_spline(x, y, k=3)  # k=3 for cubic spline
        y_smooth = spline(x_new)

        # Define custom label
        custom_label = f"Share of Germany in {sector}"

        # Plot the original data points and trend line
        plt.plot(x, y, 'o', label=f'Original Data - {custom_label}')  # Original data points
        plt.plot(x_new, y_smooth, '-', label=f'Trend Line - {custom_label}')  # Smooth trend line
    else:
        # Plot without smoothing if there are not enough data points
        plt.plot(x, y, 'o-', label=f'Original Data and Trend Line - {sector}')

# # Adding titles and labels
plt.title('Share of Germany in Primary Energy Supply by Fuel in Comparison to World Data', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Share (%)', fontsize=14)

# Set up the legend in two columns, at the bottom
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), fontsize='large', ncol=2)

plt.grid()
plt.tight_layout()

# Save the plot as an image file
plt.savefig(plot_image_path, dpi=300, bbox_inches='tight')
plt.close()  # Close the plot

print(f"Plot saved as '{plot_image_path}'")

# # Step 5: Plot a stacked area chart
# plt.figure(figsize=(24, 12))

# # Create a pivot table to prepare data for stacked area chart
# pivot_df = df.pivot(index='year', columns='sector', values='share')

# # Fill NaN values with 0 for plotting
# pivot_df.fillna(0, inplace=True)

# # Plot the stacked area chart
# plt.stackplot(pivot_df.index, pivot_df.T, labels=pivot_df.columns, alpha=0.7)

# # Adding titles and labels
# plt.title('Stacked Area Chart: Share of Germany in Primary Energy Supply by Sector', fontsize=16)
# plt.xlabel('Year', fontsize=14)
# plt.ylabel('Share (%)', fontsize=14)

# # Set up the legend
# plt.legend(loc='upper left', fontsize='large', bbox_to_anchor=(1, 1))

# plt.grid()
# plt.tight_layout()

# # Save the stacked area plot as an image file
# stacked_plot_image_path = '/home/abhijeet/GitHub/Energy/Individual Codes/Replication 1/germany_world_primary_supply_share_stacked_plot.png'  # Path for the stacked plot image
# plt.savefig(stacked_plot_image_path, dpi=300, bbox_inches='tight')
# plt.close()  # Close the plot

# print(f"Stacked area plot saved as '{stacked_plot_image_path}'")

