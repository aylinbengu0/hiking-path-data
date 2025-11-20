import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the Excel file
file_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
data = pd.read_excel(file_path)

# Define the function to extract comments from a given URL
def extract_comments(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }

    # Fetch the web page with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        return None

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the comment section
    comment_section = soup.find('ul', {'id': 'comment-list'})

    if not comment_section:
        return None

    # Extract all comments and number them
    comments = []
    for idx, comment_item in enumerate(comment_section.find_all('li'), 1):
        # Extract the comment text (description)
        desc_tag = comment_item.find('p', class_='desc')
        description = desc_tag.text.strip() if desc_tag else 'No comment text'
        comments.append(f"{idx}) {description}")

    return " - ".join(comments)  # Join all numbered comments with " - "

# Apply the function only to rows where 'Comments' column is blank
data['Comments'] = data.apply(
    lambda row: extract_comments(row['URL']) if pd.isna(row['Comments']) else row['Comments'],
    axis=1
)

# Save the updated data back to the same Excel file
data.to_excel(file_path, index=False)
