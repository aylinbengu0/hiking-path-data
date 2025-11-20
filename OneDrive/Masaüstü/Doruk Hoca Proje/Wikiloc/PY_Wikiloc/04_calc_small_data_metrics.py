import pandas as pd
import numpy as np
import os

def parse_csv(file_path):
    # Read the CSV file containing Latitude, Longitude, and Elevation
    df = pd.read_csv(file_path)
    return df

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of the Earth in meters
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

def process_csv_files(csv_directory):
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):  # Ensuring it's a CSV file
            file_path = os.path.join(csv_directory, filename)
            csv_data = parse_csv(file_path)

            distances = []
            for i in range(1, len(csv_data)):
                lat1, lon1 = csv_data.loc[i-1, 'Latitude'], csv_data.loc[i-1, 'Longitude']
                lat2, lon2 = csv_data.loc[i, 'Latitude'], csv_data.loc[i, 'Longitude']
                distances.append(haversine(lat1, lon1, lat2, lon2))

            distances.insert(0, 0)  # Start point has no distance
            csv_data['Distance'] = distances
            csv_data['Cumulative_Distance'] = csv_data['Distance'].cumsum()

            csv_data['Change_in_Latitude'] = csv_data['Latitude'].diff().fillna(0)
            csv_data['Change_in_Longitude'] = csv_data['Longitude'].diff().fillna(0)
            csv_data['Change_in_Elevation'] = csv_data['Elevation'].diff().fillna(0)

            def calculate_3d_distance(row):
                horizontal_distance = haversine(row['Latitude'], row['Longitude'],
                                                row['Latitude'] - row['Change_in_Latitude'],
                                                row['Longitude'] - row['Change_in_Longitude'])
                vertical_distance = row['Change_in_Elevation']
                return np.sqrt(horizontal_distance**2 + vertical_distance**2)

            csv_data['3D_Distance'] = csv_data.apply(calculate_3d_distance, axis=1)

            # Calculate slope as percentage
            csv_data['Slope'] = (csv_data['Change_in_Elevation'] / csv_data['3D_Distance']).replace([float('inf'), -float('inf'), np.nan], 0) * 100

            # Save the modified data back to the same CSV file
            csv_data.to_csv(file_path, index=False)
            print(f"Updated {file_path}")


# Directory path
csv_directory = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\KML_CSV_Wikiloc'  # Path to the CSV files

# Process all CSV files and overwrite them with the new data
process_csv_files(csv_directory)
