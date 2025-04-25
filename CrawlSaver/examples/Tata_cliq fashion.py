import os
import time
import json
import logging
import pandas as pd
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from CrawlSaver.checkpoint import CrawlSaver  # Automatically uses default checkpoint.txt

# === Configuration ===

URL_CSV_PATH = "/home/anusha/Desktop/DATAHUT/CrawlSaver/CrawlSaver/examples/product_urls.csv"
OUTPUT_JSON_PATH = "tata_cliq_data.json"
LOG_FILE = "Data_scraper_original.log"

# === Logging Setup ===

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# === Load URLs ===

def load_urls():
    df = pd.read_csv(URL_CSV_PATH)
    return df["url"].dropna().tolist()

# === Extraction Utilities ===

def extract_text(page, selector):
    try:
        return page.locator(selector).text_content().strip()
    except:
        return "N/A"

def extract_general_features(page):
    try:
        features = {}
        elements = page.locator(".ProductFeatures__content").all()
        for element in elements:
            headers = element.locator(".ProductFeatures__header.ProductFeatures__description").all()
            values = element.locator(".ProductFeatures__description").all()
            if len(headers) > 0 and len(values) > 1:
                key = headers[0].text_content().strip()
                value = values[1].text_content().strip()
                features[key] = value
        return features
    except Exception as e:
        logging.error(f"Error extracting general features: {e}")
        return {}


def fetch_product_details(url, page):

    try:
        logging.info(f"Scraping URL: {url}")
        page.goto(url.strip(), timeout=80000)
        page.wait_for_selector(".ProductDetailsMainCard__linkName > div:nth-child(1)", timeout=60000)

        extract = lambda selector: page.locator(selector).text_content().strip() if page.locator(selector).count() > 0 else "N/A"

        product = {
            "url": url,
            "product_name": extract(".ProductDetailsMainCard__linkName > div:nth-child(1)"),
            "brand_name": extract("#pd-brand-name > span:nth-child(1)"),
            "brand_info": extract("div.ProductDescriptionPage__detailsHolder:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1)"),
            "price": extract(".ProductDetailsMainCard__price *:not(:empty)"),
            "mrp": extract(".ProductDetailsMainCard__cancelPrice"),
            "discount": extract(".ProductDetailsMainCard__discount"),
            "rating_value": extract(".ProductDetailsMainCard__reviewElectronics[itemprop='ratingValue']"),
            "rating_count": extract(".ProductDetailsMainCard__ratingLabel[itemprop='ratingCount']"),
            "review_count": extract(".ProductDetailsMainCard__ratingLabel[itemprop='reviewCount']"),
            "product_description": extract("div.ProductDescriptionPage__detailsHolder:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"),
            "general_features": extract_general_features(page)
        }

        logging.info(f"Successfully scraped: {url}")
        return product
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return None

# === JSON Persistence ===

def save_to_json(product, json_path):
    try:
        if not os.path.exists(json_path):
            with open(json_path, 'w') as f:
                json.dump([product], f, indent=2)
        else:
            with open(json_path, 'r') as f:
                data = json.load(f)
            if not any(p["url"] == product["url"] for p in data):
                data.append(product)
                with open(json_path, 'w') as f:
                    json.dump(data, f, indent=2)
                logging.info(f"Saved to JSON: {product['url']}")
            else:
                logging.info(f"Skipped duplicate in JSON: {product['url']}")
    except Exception as e:
        logging.error(f"Error saving to JSON: {e}")

# === Main Scraping Function ===
def scrape_all():
    all_urls = load_urls()
    saver = CrawlSaver()  # default file: checkpoint.txt
    checkpoint = saver.load_checkpoint()
    start_index = 0

    # Ask user if they want to resume
    if checkpoint and saver.prompt_resume():
        start_index = checkpoint.get("index", 0)
    else:
        # If restarting: delete JSON output and reset checkpoint
        if os.path.exists(OUTPUT_JSON_PATH):
            os.remove(OUTPUT_JSON_PATH)
            logging.info("Restart selected. Existing JSON file deleted.")
        saver.save_checkpoint({"index": 0})
        start_index = 0
        logging.info("Checkpoint reset to 0.")

    logging.info(f"Starting scraping from index: {start_index}")

    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)

        for i in range(start_index, len(all_urls)):
            url = all_urls[i]
            if not url.startswith("http"):
                logging.warning(f"Skipping invalid URL: {url}")
                continue

            product = fetch_product_details(url, page)
            if product:
                save_to_json(product, OUTPUT_JSON_PATH)

            # Save checkpoint after each URL
            saver.save_checkpoint({"index": i + 1})
            time.sleep(2)

        browser.close()

    logging.info("Scraping process completed successfully.")


# === Entry Point ===

if __name__ == "__main__":
    scrape_all()

    
