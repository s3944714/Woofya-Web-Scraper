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
url = "https://www.auski.com.au/blogs/news/27-best-dog-friendly-camping-spots-in-nsw"

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

        # Find all locations and their descriptions
        locations = soup.find_all('div', class_='shg-rich-text shg-theme-text-content')

        camping_spots = []

        # Loop through each location and extract the h3 (location name) and p (description)
        for location in locations:
            # Extract the location name from <h3>
            location_names = location.find_all('h3')
            descriptions = location.find_all('p')

            for name, desc in zip(location_names, descriptions):
                location_name = name.text.strip()
                description_text = desc.text.strip()

                # Append the camping spot details to the list
                camping_spots.append({
                    'Location Name': location_name,
                    'Description': description_text
                })

        # Save the data to a JSON file in the Raw_Data folder
        output_file_path = os.path.join(raw_data_folder, 'dog_friendly_camping_spots_nsw.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(camping_spots, f, ensure_ascii=False, indent=4)

        print(f"Scraped data has been saved to {output_file_path}")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
