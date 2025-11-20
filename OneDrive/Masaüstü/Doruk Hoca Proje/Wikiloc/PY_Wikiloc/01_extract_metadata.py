import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'
}

# URL of the website
url = 'https://www.wikiloc.com/hiking-trails/sarek-national-park-sweden-1136840'

# Send a GET request with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract trail name from h1
    trail_div = soup.find('div', class_='view__header__title')
    trail_name = None
    if trail_div:
        trail_name = trail_div.find('h1').get_text()
        print(f"Trail Name: {trail_name}")
    else:
        print("Could not find the trail name element in the page.")

    # Extract region and locality from breadcrumb (e.g., 'Australia' and 'Sunshine Beach')
    breadcrumb_nav = soup.find('nav', class_='view__header__breadcrumb__links')
    region, locality = None, None
    if breadcrumb_nav:
        breadcrumb_spans = breadcrumb_nav.find_all('span')
        if len(breadcrumb_spans) >= 2:
            region = breadcrumb_spans[0].get_text()  # Extract the region (first span)
            locality = breadcrumb_spans[-1].get_text()  # Extract the locality (last span)
            print(f"Region: {region}")
            print(f"Locality: {locality}")
        else:
            print("Could not find sufficient breadcrumb span elements.")
    else:
        print("Could not find the breadcrumb navigation in the page.")

    # Extract description from the Itinerary description section
    description_div = soup.find('div', class_='description')
    description_text = None
    if description_div:
        description_text = description_div.get_text(separator=' ', strip=True)
        print(f"Description: {description_text}")
    else:
        print("Could not find the description section in the page.")

    # Proceed with updating the Excel file if all values are found
    if trail_name and region and locality and description_text:
        # File path to the Excel file
        file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'

        # Load the Excel file
        df = pd.read_excel(file_path)

        # Find the first blank row in the "Title" column
        last_blank_title_row = df[df['Title'].isna()].index[0]

        # Add the trail name to the last blank row under the "Title" column
        df.at[last_blank_title_row, 'Title'] = trail_name

        # Find the first blank row in the "Region" column
        last_blank_region_row = df[df['Region'].isna()].index[0]

        # Add the region to the last blank row under the "Region" column
        df.at[last_blank_region_row, 'Region'] = region

        # Find the first blank row in the "Locality" column
        last_blank_locality_row = df[df['Locality'].isna()].index[0]

        # Add the locality to the last blank row under the "Locality" column
        df.at[last_blank_locality_row, 'Locality'] = locality

        # Find the first blank row in the "Description" column
        last_blank_description_row = df[df['Description'].isna()].index[0]

        # Add the description to the last blank row under the "Description" column
        df.at[last_blank_description_row, 'Description'] = description_text

        # Find the first blank row in the "URL" column
        last_blank_url_row = df[df['URL'].isna()].index[0]

        # Add the URL to the last blank row under the "URL" column
        df.at[last_blank_url_row, 'URL'] = url

        # Save the updated file back
        df.to_excel(file_path, index=False)

        print(
            f"Trail name '{trail_name}', region '{region}', locality '{locality}', description, and URL added to the Excel file.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
