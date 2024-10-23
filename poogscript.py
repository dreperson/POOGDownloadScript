import requests
from bs4 import BeautifulSoup
import os

# Function to download file from a given URl
def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error occurred while downloading {url}: {e}")

# Function to scrape the webpage and download files
def scrape_and_download(url, destination_folder):
    # Get the webpage content
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all the podcast episode links
    links = soup.find_all('a', class_='episode-link', title='Download')

    # Reverse the list to start from the bottom episode
    links = links[::-1]

    # Counter to generate file prefixes
    file_counter = 1

    # Loop through the reversed list of links and download them
    for link in links:
        href = link.get('href')
        if href: 
            file_url = href if href.startswith('http') else url + href

            # Extract the original filename from the URL
            original_filename = os.path.basename(href)
            file_extension = os.path.splitext(original_filename)[-1]

            #Create new file name with counter
            file_prefix = f"{file_counter:03}"
            new_filename = f"{file_prefix}{original_filename}"
            save_path = os.path.join(destination_folder, new_filename)

            # Download the file
            download_file(file_url, save_path)

            # Increment the counter for the next file
            file_counter += 1

# Example usage
if __name__ == "__main__":
    target_url = "https://podcastindex.org/podcast/1365697"
    destination_dir = r"C:\Users\drepe\Documents\POOG Archive"

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Scrape and download files
    scrape_and_download(target_url, destination_dir)