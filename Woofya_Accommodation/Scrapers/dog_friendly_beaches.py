import requests
from bs4 import BeautifulSoup
import json
import os

# Define the path to the Raw_Data folder
BASE = os.path.dirname(os.path.abspath(__file__))
raw_data_folder = os.path.join(BASE, 'Raw_Data')

# Ensure the Raw_Data folder exists
if not os.path.exists(raw_data_folder):
    os.makedirs(raw_data_folder)

# URL of the webpage to scrape
url = "https://www.dogzone.com.au/dog-friendly-camping-australia/"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Send a GET request to the webpage
try:
    response = requests.get(url, headers=headers, timeout=15)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all camping sections (example assumes sections are within <p> tags for this use case)
        camping_sections = soup.find_all('p')

        dog_friendly_camps = []

        # Loop through each camping section to extract details
        for section in camping_sections:
            # Extract the site name and URL (assuming structure is as in your example)
            site_name = section.text.strip().split("\n")[0]  # Get the name before the break
            link_tag = section.find('a')  # Extract the URL link

            if link_tag:
                site_url = link_tag['href'] if 'href' in link_tag.attrs else 'No URL available'
            else:
                site_url = 'No URL available'

            # Add custom fields
            features = "Never Leave your Dog Unattended, Obedience"
            identification = "Collar and Leash"
            on_leash_policy = "On Leash Policy"

            # Append the campsite details to the list
            dog_friendly_camps.append({
                'Site Name': site_name,
                'URL': site_url,
                'Features': features,
                'Identification': identification,
                'On Leash Policy': on_leash_policy
            })

        # Save the data to a JSON file in the Raw_Data folder
        output_file_path = os.path.join(raw_data_folder, 'dog_friendly_camps.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(dog_friendly_camps, f, ensure_ascii=False, indent=4)

        print(f"Scraped data has been saved to {output_file_path}")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
