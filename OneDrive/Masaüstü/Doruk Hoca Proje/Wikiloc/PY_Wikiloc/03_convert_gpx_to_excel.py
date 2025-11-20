import os
import xml.etree.ElementTree as ET
import pandas as pd

def extract_kml_to_csv(kml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the correct namespace for this specific KML version
    namespaces = {'kml': 'http://earth.google.com/kml/2.0'}

    # Loop over all files in the KML folder
    for filename in os.listdir(kml_folder):
        if filename.endswith(".kml"):
            kml_file_path = os.path.join(kml_folder, filename)
            csv_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")

            try:
                # Parse the KML file
                tree = ET.parse(kml_file_path)
                root = tree.getroot()

                # List to hold extracted coordinate data
                coordinates = []

                # Extract coordinates (look for Placemark > LineString > coordinates)
                for placemark in root.findall('.//kml:Placemark', namespaces):
                    for linestring in placemark.findall('.//kml:LineString/kml:coordinates', namespaces):
                        coord_text = linestring.text.strip()
                        for line in coord_text.split():
                            lon, lat, elev = map(float, line.split(','))
                            coordinates.append([lat, lon, elev])

                # Check if coordinates were found
                if coordinates:
                    # Create a DataFrame from the coordinates
                    df = pd.DataFrame(coordinates, columns=['Latitude', 'Longitude', 'Elevation'])

                    # Save the DataFrame to CSV
                    df.to_csv(csv_file_path, index=False)
                    print(f"Saved {csv_file_path}")
                else:
                    print(f"No coordinates found in {filename}")

            except ET.ParseError as e:
                print(f"KML parsing error in {filename}: {e}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Example directories (adjust paths as needed)
kml_folder = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\KML_Downloads_Wikiloc'
output_folder = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\KML_CSV_Wikiloc'

extract_kml_to_csv(kml_folder, output_folder)
