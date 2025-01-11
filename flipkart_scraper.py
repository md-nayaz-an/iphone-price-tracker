from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_scraper import BaseScraper

class FlipkartScraper(BaseScraper):
    def fetch_price(self, url):
        self.driver.get(url)
        try:
            price_tag = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="Nx9bqj CxhGGd"]'))
            )
            if price_tag:
                price = price_tag.text.strip().replace(",", "").replace("₹", "")
                self.save_to_csv("iPhone 16 Pro Max", price, "Flipkart")  # Call to save price
                return price
        except Exception as e:
            print(f"Error fetching price from Flipkart: {e}")
        return None
