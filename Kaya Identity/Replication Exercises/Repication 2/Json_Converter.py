import json
import csv
from datetime import datetime, timezone
import os
import re

# Function to clean the 'name' field and convert Unix timestamp to year
def clean_data(entry):
    # Clean the name and remove unwanted words, then strip any extra whitespace and commas
    cleaned_name = re.sub(r'\s*(Germany|Annual|World)\s*', ' ', entry['name']).strip()
    cleaned_name = re.sub(r',\s*,+', ',', cleaned_name)  # Remove duplicate commas
    cleaned_name = re.sub(r',\s*$', '', cleaned_name)  # Remove trailing comma
    cleaned_data = [
        {'date': datetime.fromtimestamp(item['date'] / 1000, tz=timezone.utc).year, 'value': item['value']}
        for item in entry['data'] if item['value'] not in {'--', ''}
    ]
    return {'name': cleaned_name, 'data': cleaned_data} if cleaned_data else None

# Function to filter and clean JSON data
def clean_json_data(json_file, cleaned_json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    filtered_data = [clean_data(entry) for entry in data]
    filtered_data = [entry for entry in filtered_data if entry]  # Remove None entries

    with open(cleaned_json_file, 'w') as outfile:
        json.dump(filtered_data, outfile, indent=4)

    print(f"Filtered JSON saved to {cleaned_json_file}")

# Function to convert JSON data to CSV
def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    fieldnames = ['Year'] + [entry['name'] for entry in data]
    year_data = {}

    for entry in data:
        for record in entry['data']:
            year_data.setdefault(record['date'], {})[entry['name']] = record['value']

    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for year, row_data in sorted(year_data.items()):
            # Prepare row, replacing empty values with ''
            row = {'Year': year, **{name: row_data.get(name, '') for name in fieldnames[1:]}}
            # Write row only if it has at least one non-empty field
            if any(value not in {"", "--"} for value in row_data.values()):
                writer.writerow(row)

    print(f"CSV file saved to {csv_file}")

# Main function to clean JSON and convert to CSV
def process_energy_consumption_data(input_json_file):
    base_name = os.path.splitext(os.path.basename(input_json_file))[0]
    cleaned_json_file = f"clean_{base_name}.json"
    output_csv_file = f"clean_{base_name}.csv"
    
    clean_json_data(input_json_file, cleaned_json_file)
    json_to_csv(cleaned_json_file, output_csv_file)

# Example usage
input_json_file = 'World Elec Gen.json'  # Replace with your JSON file path
process_energy_consumption_data(input_json_file)
