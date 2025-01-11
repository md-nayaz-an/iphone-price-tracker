from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_scraper import BaseScraper

class ControlzScraper(BaseScraper):
    def fetch_price(self, url):
        self.driver.get(url)
        try:
            price_tag = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="price-item price-item--sale price-item--last"]'))
            )
            if price_tag:
                price = price_tag.text.strip().replace(",", "").replace("₹", "")
                self.save_to_csv("iPhone 16 Pro Max", price, "Controlz")  # Call to save price
                return price
        except Exception as e:
            print(f"Error fetching price from Controlz: {e}")
        return None
