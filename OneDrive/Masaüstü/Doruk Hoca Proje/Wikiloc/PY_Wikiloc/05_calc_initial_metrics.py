import pandas as pd
import os

# Load the Excel file into a DataFrame
excel_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
hikes_data = pd.read_excel(excel_path)

def analyze_csv_data(file_path):
    csv_data = pd.read_csv(file_path)
    # Debugging step: Print the elevation data and its statistics
    print(f"Analyzing {file_path}")
    print(csv_data['Elevation'].describe())
    print(csv_data['Elevation'].head(10))  # Print the first 10 values for a quick check
    total_length = float(round(csv_data['Cumulative_Distance'].iloc[-1], 1))
    highest_point = float(round(csv_data['Elevation'].max(), 1))
    lowest_point = float(round(csv_data['Elevation'].min(), 1))
    return (total_length, highest_point, lowest_point)

directory_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\KML_CSV_Wikiloc'
files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

# Process each .csv file in the directory
for file in files:
    file_id = int(file.split('.')[0])  # Assuming the file name format is 'ID.csv'
    results = analyze_csv_data(os.path.join(directory_path, file))
    # Find the row with the matching ID and update it with the new data
    row_index = hikes_data[hikes_data['ID'] == file_id].index
    if not row_index.empty:
        hikes_data.loc[row_index, 'Total Length (km)'] = results[0]
        hikes_data.loc[row_index, 'Highest Point (m)'] = results[1]
        hikes_data.loc[row_index, 'Lowest Point (m)'] = results[2]

# Save the updated DataFrame back to the Excel file
hikes_data.to_excel(excel_path, index=False)
