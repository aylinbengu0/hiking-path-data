import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: Load Excel file and get URLs
file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'  # Your file path
df = pd.read_excel(file_path)

# Step 2: Function to scrape the "Technical difficulty" from the webpage
def scrape_difficulty(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find the "Technical difficulty" field
            difficulty_element = soup.find('dt', string='Technical difficulty')
            if difficulty_element:
                difficulty = difficulty_element.find_next('dd').text.strip()
                return difficulty
            else:
                return 'Technical difficulty not found'
        else:
            return f"Error: Status code {response.status_code}"

    except Exception as e:
        # Return the exception message in case of failure
        return f"Error: {str(e)}"


# Step 3: Apply the scraping function only to rows where 'Technical difficulty' column is blank
df['Technical difficulty'] = df.apply(
    lambda row: scrape_difficulty(row['URL']) if pd.isna(row['Technical difficulty']) else row['Technical difficulty'],
    axis=1
)

# Step 4: Save the updated DataFrame to the same Excel file
output_file = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Scraped data saved to {output_file}")