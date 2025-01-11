import argparse
import json
from selenium import webdriver
from amazon_scraper import AmazonScraper
from flipkart_scraper import FlipkartScraper
from cashify_scraper import CashifyScraper
from controlz_scraper import ControlzScraper

# Load platform URLs from the configuration file
with open("platform_urls.json", "r") as file:
    platform_urls = json.load(file)

# Define the argument parser
parser = argparse.ArgumentParser(description="Run scraper for a specific platform.")
parser.add_argument("-p", "--platform", type=str, required=True, help="Platform to scrape (Amazon, Flipkart, Cashify, Controlz)")
args = parser.parse_args()

# Initialize Chrome WebDriver with options (headless mode)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# Map platforms to their respective scraper classes
scrapers = {
    "amazon": AmazonScraper(driver),
    "flipkart": FlipkartScraper(driver),
    "cashify": CashifyScraper(driver),
    "controlz": ControlzScraper(driver)
}

platform = args.platform.lower()

# Run the scraper for the specified platform
if platform in scrapers:
    scraper = scrapers[platform]
    url = platform_urls.get(platform)
    if url:
        print(f"Fetching price for {platform}...")
        price = scraper.fetch_price(url)
        if price:
            print(f"Fetched price: ₹{price}")
        else:
            print(f"Failed to fetch price for {platform}.")
    else:
        print(f"URL for {platform} not found in configuration file.")
else:
    print(f"Platform {platform} is not supported.")

driver.quit()
