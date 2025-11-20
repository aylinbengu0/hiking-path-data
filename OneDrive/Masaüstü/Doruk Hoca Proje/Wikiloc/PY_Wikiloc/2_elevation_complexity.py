import os
import pandas as pd


def process_gpx_data(file_path):
    try:
        data = pd.read_csv(file_path)
        # Calculate various metrics
        data['Slope'] = (data['Change_in_Elevation'] / data['3D_Distance']).replace(
            [float('inf'), -float('inf'), float('nan')], 0) * 100
        elevation_gain = data['Change_in_Elevation'][data['Change_in_Elevation'] > 0].sum()
        elevation_loss = data['Change_in_Elevation'][data['Change_in_Elevation'] < 0].sum()
        steep_threshold = 10
        data['Steep'] = abs(data['Slope']) > steep_threshold
        num_steep_segments = data['Steep'].sum()

        # Continuous Elevation Gain
        data['Positive_Gain'] = data['Change_in_Elevation'] > 0
        data['Gain_Group'] = (data['Positive_Gain'] != data['Positive_Gain'].shift(1)).cumsum()
        positive_gain_groups = data[data['Positive_Gain'] == True].groupby('Gain_Group').agg(
            Start=pd.NamedAgg(column='Cumulative_Distance', aggfunc='first'),
            End=pd.NamedAgg(column='Cumulative_Distance', aggfunc='last'),
            Total_Gain=pd.NamedAgg(column='Change_in_Elevation', aggfunc='sum'),
            Distance=pd.NamedAgg(column='3D_Distance', aggfunc='sum')
        )
        longest_gain_section = positive_gain_groups.loc[
            positive_gain_groups['Distance'].idxmax()] if not positive_gain_groups.empty else {}
        most_gain_section = positive_gain_groups.loc[
            positive_gain_groups['Total_Gain'].idxmax()] if not positive_gain_groups.empty else {}

        # Direction Changes
        data['Elevation_Direction'] = data['Change_in_Elevation'].apply(
            lambda x: 'Up' if x > 0 else ('Down' if x < 0 else 'Flat'))
        data['Direction_Change'] = (data['Elevation_Direction'] != data['Elevation_Direction'].shift(1))
        number_of_changes = data['Direction_Change'].sum()

        # Collect results
        results = {
            'Elevation Gain': round(elevation_gain, 2),
            'Elevation Loss': round(elevation_loss, 2),
            'Steep Sections': num_steep_segments,
            'Longest Gain Section Total Gain': round(longest_gain_section.get('Total_Gain', 0), 2),
            'Longest Gain Section Distance': round(longest_gain_section.get('Distance', 0), 2),
            'Most Gain Section Total Gain': round(most_gain_section.get('Total_Gain', 0), 2),
            'Most Gain Section Distance': round(most_gain_section.get('Distance', 0), 2),
            'Direction Changes': number_of_changes,
        }
        return results
    except Exception as e:
        print(f"Failed to process file {file_path}: {e}")
        return None  # In case of failure


def main():
    data_folder_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\KML_CSV_Wikiloc'
    output_file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'

    # Load the main hiking data
    main_hiking_data = pd.read_excel(output_file_path)

    # List of all CSV files in the folder
    files = [os.path.join(data_folder_path, f) for f in os.listdir(data_folder_path) if f.endswith('.csv')]

    # Process each file
    for file in files:
        file_id = int(os.path.basename(file).split('.')[0])  # Assuming the file name format is 'ID.csv'
        results = process_gpx_data(file)
        if results:
            # Find the row with the matching file ID
            row_index = main_hiking_data[main_hiking_data['ID'] == file_id].index
            if not row_index.empty:
                for key, value in results.items():
                    main_hiking_data.loc[row_index, key] = value

    # Ensure proper data types and rounding for float columns (keeping NaN values)
    decimal_cols = [
        'Elevation Gain', 'Elevation Loss', 'Longest Gain Section Total Gain',
        'Longest Gain Section Distance', 'Most Gain Section Total Gain', 'Most Gain Section Distance',
        'Steep Sections', 'Direction Changes'
    ]

    # Round float values while preserving NaN
    for col in decimal_cols:
        main_hiking_data[col] = main_hiking_data[col].round(2)

    # Save the updated Excel file, keeping NaN values
    main_hiking_data.to_excel(output_file_path, index=False)


if __name__ == "__main__":
    main()
