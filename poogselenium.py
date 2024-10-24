import os
import geckodriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import time
import requests

# Automatically install geckodriver
geckodriver_autoinstaller.install()

# Function to download file from a given URL
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
        print(f"Error occurred while downloading: {url}: {e}")

# Function to scrape the webpage and download files
def scrape_and_download(url, destination_folder):
    try:
        # Set up the Selenium WebDriver for Firefox
        service = Service()
        driver = webdriver.Firefox(service=service)

        # Load the page
        driver.get(url)
        time.sleep(3) # Give the page time to load JavaScript content

        #Scroll to the bottom to load all elements
        last_height = driver.execute_script("return document.body.scrollHeight")
        while  True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # Wait for the document to load

            # Calculate new scroll height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get the page source after it is fully rendered
        page_source = driver.page_source

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all the podcast episode download links
        links = soup.find_all('a', class_='episode-link', title='Download')

        print(f"Found {len(links)} download links")

        if not links:
            print("No download links found with the provided class and title.")
            return
        
        # Reverse from the list to start from the bottom episode
        links = links[::-1]

        # Counter to generate file prefixes
        file_counter = 1

        # Loop through the reversed list of links and downlaod them
        for link in links:
            href = link.get('href')
            if href:
                file_url = href if href.startswith('http') else url + href

                # Extract the original filename from the URL without query parameters
                original_filename = os.path.basename(href.split('?')[0])

                # Create new file name with counter
                file_prefix = f"{file_counter:03}"
                new_filename = f"{file_prefix}{original_filename}"
                save_path = os.path.join(destination_folder, new_filename)

                # Download the file
                download_file(file_url, save_path)

                # Increment the counter for the next file
                file_counter += 1
            else:
                print(f"Link with no href found: {link}")
        
        # Close the browser
        driver.quit()

    except Exception as e:
        print(f"Error occurred while scraping {url}: {e}")

# Example usage
if __name__ == "__main__":
    target_url = "https://podcastindex.org/podcast/1365697"
    destination_dir = r"C:\Users\drepe\Documents\POOG Archive"

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Scrape and download files
    scrape_and_download(target_url, destination_dir)