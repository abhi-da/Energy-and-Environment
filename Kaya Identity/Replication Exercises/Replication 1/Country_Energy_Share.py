import pandas as pd
import matplotlib.pylab as plt
import json
import numpy as np
from scipy.interpolate import CubicSpline

# Load the cleaned primary energy supply data from JSON
country = 'Germany'  # Change country if needed
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

# Specify the correct column name for total energy consumption
total_energy_consumption_col = 'Total energy consumption'  # Adjust if needed

# Exclude certain columns for share calculation
pivot_df.columns = pivot_df.columns.str.strip().str.lower()
total_energy_consumption_col = total_energy_consumption_col.strip().lower()
columns_excluded = ['year', total_energy_consumption_col, 'total energy consumption from nuclear, renewables, and other'.strip().lower()]

# Filter columns that are not in the excluded list
columns_sum = [col for col in pivot_df.columns if col not in columns_excluded]

# Calculate shares for each sector
for col in columns_sum:
    pivot_df[col + ' share'] = (pivot_df[col] / pivot_df[total_energy_consumption_col]) * 100

# # Extract share columns for plotting
share_columns = [col for col in pivot_df.columns if col.endswith('share')]

# # Set a color palette
# colors = plt.cm.tab10(np.linspace(0, 1, len(share_columns)))

# # Stacked area chart for primary energy supply shares
# plt.figure(figsize=(40, 12))
# pivot_df.plot(x='year', y=share_columns, kind='area', stacked=True, color=colors, alpha=0.7)

# # Overlay trend lines for each sector's share using cubic spline interpolation
# for col, color in zip(share_columns, colors):
#     # Cubic spline interpolation
#     cs = CubicSpline(pivot_df['year'], pivot_df[col])
#     years_smooth = np.linspace(pivot_df['year'].min(), pivot_df['year'].max(), 500)
#     plt.plot(years_smooth, cs(years_smooth), linestyle='-', linewidth=2, alpha=0.8, color='black')

# plt.title(f'{country} Primary Energy Supply Share by Fuel', fontsize=14, fontweight='bold')
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('Share (%)', fontsize=12)

# # Customize the legend with formatted names
# formatted_share_labels = [f'Share of {col.replace(" share", "")}' for col in share_columns]
# plt.legend(formatted_share_labels, loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize='medium', title='Primary Energy Supply Shares', title_fontsize='medium')

# # Customize grid lines
# plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# # Tight layout and save the stacked area chart
# plt.tight_layout()
# plt.savefig('Primary_Energy_Supply_Share_Trend line.png', dpi=600)
# plt.close()

# # Title and labels
# plt.title(f'{country} Primary Energy Supply Share by Fuel Over Time', fontsize=14, fontweight='bold')
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('Share (%)', fontsize=12)

# # Customize the legend with formatted names
# formatted_share_labels = [f'Share of {col.replace(" share", "")}' for col in share_columns]
# plt.legend(formatted_share_labels, loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize='medium', title='Primary Energy Supply Shares', title_fontsize='medium')

# # Customize grid lines
# plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# # Tight layout and save
# plt.tight_layout()
# plt.savefig('Primary_Energy_Supply_Share_Stacked_Area.png', dpi=600)
# plt.close()

# # Calculate the growth rate for total energy consumption and other sectors
# growth_rate_columns = columns_sum  # Adjust this if needed
# for col in growth_rate_columns:
#     pivot_df[col + ' Growth Rate'] = pivot_df[col].pct_change() * 100

# # Prepare to plot growth rates
# plt.figure(figsize=(20, 12))
# for col in growth_rate_columns:
#     plt.plot(pivot_df['year'], pivot_df[col + ' Growth Rate'], marker='o', label=f'Growth Rate of {col}', alpha=0.9)

# # Title and labels
# plt.title(f'{country} Primary Energy Supply Growth Rates by Source Over Time', fontsize=14, fontweight='bold')
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('Growth Rate (%)', fontsize=12)

# # Customize the legend
# plt.legend(loc='lower center', fontsize='medium')

# # Customize grid lines
# plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# # Tight layout and save
# plt.tight_layout()
# plt.savefig('Primary_Energy_Supply_Growth_Rates.png', dpi=300)
# plt.close()

# Calculate the growth rate for total energy consumption and other sectors
growth_rate_columns = columns_sum  # Adjust this if needed
for col in growth_rate_columns:
    pivot_df[col + ' Growth Rate'] = pivot_df[col].pct_change() * 100

# Prepare to plot growth rates
plt.figure(figsize=(20, 12))
for col in growth_rate_columns:
    plt.plot(pivot_df['year'], pivot_df[col + ' Growth Rate'], marker='o', label=f'Growth Rate of {col}', alpha=0.9)

# Title and labels
plt.title(f'{country} Primary Energy Supply Growth Rates by Source Over Time', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Growth Rate (%)', fontsize=12)

# Customize the legend
plt.legend(loc='lower center', fontsize='medium')

# Customize grid lines
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Tight layout and save
plt.tight_layout()
plt.savefig('Primary_Energy_Supply_Growth_Rates.png', dpi=1000)
plt.close()

# Set a color palette
colors = plt.cm.tab10(np.linspace(0, 1, len(share_columns)))

# Create a figure and axis with constrained layout
fig, ax = plt.subplots(figsize=(25, 12), constrained_layout=True)  # Use constrained_layout

# Plot the stacked area chart and get handles
area_patches = pivot_df.plot(x='year', y=share_columns, kind='area', stacked=True, color=colors, alpha=0.7, ax=ax)

# Title and labels
plt.title(f'{country} Primary Energy Supply Share by Fuel', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Share (%)', fontsize=12)

ax.set_xticks(np.arange(pivot_df['year'].min(), pivot_df['year'].max() + 1, step=1))  # Adjust step value for ticks
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))  # Ensure x-ticks are formatted as integers

# Customize the y-axis to show a wider range of percentages
ax.set_ylim(0, 100)  # Set the y-axis limit to range from 0% to 100%

# Customize the legend
handles, labels = ax.get_legend_handles_labels()  # Get the handles and labels for the legend
formatted_share_labels = [f'Share of {label.replace(" share", "")}' for label in labels]
legend = ax.legend(handles, formatted_share_labels, loc='lower center', fontsize='medium', title='Primary Energy Supply Shares', handlelength=1.5, borderaxespad=0)

# Adjust legend size and position
legend.set_bbox_to_anchor((0.5, -0.2))  # Adjust bbox_to_anchor for legend placement

# Set legend title font size
legend.get_title().set_fontsize('medium')

# Customize grid lines
ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Save the stacked area chart
plt.savefig('Primary_Energy_Supply_Share_Stacked_Area.png', dpi=1000)
plt.close()



# Prepare to plot trend of share percentages


# Prepare to plot trend of share percentages
plt.figure(figsize=(25, 15))

# Overlay trend lines for each sector's share using cubic spline interpolation
for col, color in zip(share_columns, colors):
    # Cubic spline interpolation
    cs = CubicSpline(pivot_df['year'], pivot_df[col])
    years_smooth = np.linspace(pivot_df['year'].min(), pivot_df['year'].max(), 500)
    
    # Plot the trend line for the sector's share
    plt.plot(years_smooth, cs(years_smooth), linestyle='-', linewidth=2, color=color, alpha=0.9, label=f'Trend of {col.replace(" share", "")}')

# Title and labels
plt.title(f'{country} Primary Energy Supply Share Percentage Trends by Fuel', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Share (%)', fontsize=12)

# Set x-axis ticks to show more years
plt.xticks(np.arange(pivot_df['year'].min(), pivot_df['year'].max() + 1, step=1))  # Adjust step value for ticks
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))  # Ensure x-ticks are formatted as integers

# Customize the y-axis to show a wider range of percentages
plt.ylim(0, 60)  # Set the y-axis limit to range from 0% to 100%

# Customize the legend
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), fontsize='medium', title='Fuel Share Trends', title_fontsize='medium')

# Customize grid lines
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Tight layout and save the trend chart
plt.tight_layout(rect=[0, 0, 1, 0.9])  # Adjust to allow space for the legend
plt.savefig('Primary_Energy_Supply_Share_Percentage_Trends.png', dpi=300)
plt.close()

# Prepare to plot the trend of primary energy supply values
plt.figure(figsize=(25, 12))

# Plot each sector's primary energy supply trend
for col in columns_sum:
    plt.plot(pivot_df['year'], pivot_df[col], marker='o', label=f'{col}', alpha=0.9)

# Title and labels
plt.title(f'{country} Primary Energy Supply Trends by Sector', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Primary Energy Supply (qbtu)', fontsize=12)  # Adjust units as needed

# Set x-axis ticks to show more years
plt.xticks(np.arange(pivot_df['year'].min(), pivot_df['year'].max() + 1, step=1))  # Adjust step value for ticks
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))  # Ensure x-ticks are formatted as integers

# Customize the legend
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), fontsize='medium', title='Energy Supply by Sector')

# Customize grid lines
plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Tight layout and save the trend chart
plt.tight_layout()
plt.savefig('Primary_Energy_Supply_Trends.png', dpi=300)
plt.close()



# Export final data
pivot_df_final = pivot_df[['year'] + share_columns]
pivot_df_final.to_csv('Primary_Energy_Supply_Shares.csv', index=False)
pivot_df_final.to_json('Primary_Energy_Supply_Shares.json', orient='records')
