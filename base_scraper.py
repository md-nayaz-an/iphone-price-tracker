import csv
import os
from datetime import datetime

class BaseScraper:
    def __init__(self, driver):
        self.driver = driver

    def fetch_price(self, url):
        raise NotImplementedError("Subclasses must implement the fetch_price method")

    def save_to_csv(self, product, price, platform):
        # Create a data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)

        # Define the CSV file path for the platform
        csv_file = f"data/{platform.lower()}_prices.csv"

        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")

        # Read existing data to update or append
        existing_data = {}
        if os.path.exists(csv_file):
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_name = row["Product"]
                    if product_name not in existing_data:
                        existing_data[product_name] = {}
                    for date, price in row.items():
                        if date != "Product":
                            existing_data[product_name][date] = price

        # Update or add today's price for the specified product
        if product not in existing_data:
            existing_data[product] = {}
        existing_data[product][today] = price

        # Write back to CSV file (overwriting)
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            # Prepare header (dates)
            header = ["Product"] + sorted({date for dates in existing_data.values() for date in dates.keys()})
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            # Write each product's prices under their respective dates
            for product_name, prices in existing_data.items():
                row = {"Product": product_name}
                row.update(prices)  # Add prices for each date
                writer.writerow(row)

        print(f"Updated prices saved to {csv_file}.")
