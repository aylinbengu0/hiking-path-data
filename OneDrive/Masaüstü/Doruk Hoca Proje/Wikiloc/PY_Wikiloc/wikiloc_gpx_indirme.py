import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


def download_gpx(data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    results = []

    for index, row in data.iterrows():
        url = row['URL']
        hike_id = row['ID']
        try:
            # Access the page with the download options
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                download_page_url = urljoin(url, f"/wikiloc/download.do?id={hike_id}")

                # Fetch the download options page
                download_page_response = requests.get(download_page_url, headers=headers)
                if download_page_response.status_code == 200:
                    # Send the form data to get the file
                    form_data = {
                        'selFormat': 'gpx',  # Select GPX format
                        'filter': 'original',  # Select original track points
                        'includeDisplayed': 'false'
                    }
                    download_response = requests.post(download_page_url, data=form_data, headers=headers, stream=True)

                    # Save the GPX file
                    if download_response.status_code == 200:
                        file_path = os.path.join(output_folder, f"{str(hike_id).zfill(2)}.gpx")
                        with open(file_path, 'wb') as file:
                            for chunk in download_response.iter_content(chunk_size=1024):
                                if chunk:
                                    file.write(chunk)
                        results.append(f"Downloaded: {file_path}")
                    else:
                        results.append(f"Failed to download GPX - Status code: {download_response.status_code}")
                else:
                    results.append(
                        f"Failed to access download options page - Status code: {download_page_response.status_code}")
            else:
                results.append(f"Failed to access hike page - Status code: {response.status_code}")
        except Exception as e:
            results.append(f"Error processing {url}: {str(e)}")

    return results


# Load your Excel file
import pandas as pd

file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
df = pd.read_excel(file_path)

# Directory to save the downloaded GPX files
output_directory = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\GPX_Downloads_Wikiloc'

# Start the download process
download_results = download_gpx(df, output_directory)
print(download_results)
