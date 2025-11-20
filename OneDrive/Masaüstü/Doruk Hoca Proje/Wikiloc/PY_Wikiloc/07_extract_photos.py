import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Set up Selenium options (this avoids opening the browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Specify the path to Chrome executable and ChromeDriver
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome-win64\chrome.exe"
webdriver_service = Service(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver-win64\chromedriver.exe')

# Initialize the WebDriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Read the Excel file
file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
df = pd.read_excel(file_path)

# Ensure there's a 'URL' column and a 'Photo URLs' column
if 'URL' in df.columns:
    if 'Photo URLs' not in df.columns:
        df['Photo URLs'] = ''  # Initialize the 'Photo URLs' column if missing

    # Loop over each row in the DataFrame
    for index, row in df.iterrows():
        base_url = row['URL']
        photo_urls = row['Photo URLs']

        # Skip rows that already have Photo URLs filled
        if pd.notna(photo_urls) and photo_urls.strip():
            print(f"Skipping row {index} as 'Photo URLs' is already filled.")
            continue

        if pd.isna(base_url):
            print(f"Skipping row {index} due to missing URL.")
            continue

        print(f"Processing URL: {base_url}")

        try:
            # Open the webpage
            driver.get(base_url)
            driver.implicitly_wait(10)  # Wait for the page to fully load

            # Find the "View more photos" button
            view_more_button = driver.find_element(By.CSS_SELECTOR, 'button.trail__images__cta')

            if view_more_button:
                # Extract the URL from the onclick attribute
                onclick_value = view_more_button.get_attribute('onclick')
                start = onclick_value.find("location.href = '") + len("location.href = '")
                end = onclick_value.find("';")
                new_url = onclick_value[start:end]

                print(f"Redirecting to URL: {new_url}")

                # Navigate to the new URL
                driver.get(new_url)
                time.sleep(5)  # Wait for the new page to load

                # Get the data-id attributes from the photo thumbnails
                photo_elements = driver.find_elements(By.CSS_SELECTOR, 'li[data-id]')
                photo_ids = [element.get_attribute('data-id') for element in photo_elements]

                if photo_ids:
                    # Create photo URLs
                    photo_urls = [f"{base_url}/photo-{photo_id}" for photo_id in photo_ids]
                    df.at[index, 'Photo URLs'] = ','.join(photo_urls)
                else:
                    print(f"No photo IDs found for {new_url}")
            else:
                print(f"'View more photos' button not found for {base_url}")

        except Exception as e:
            print(f"Error processing URL {base_url}: {e}")

else:
    print("The 'URL' column is missing in the Excel file.")

# Save the updated DataFrame back to the Excel file
output_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
df.to_excel(output_path, index=False)

# Close the WebDriver
driver.quit()

print(f"Photo URLs added and saved to {output_path}")
