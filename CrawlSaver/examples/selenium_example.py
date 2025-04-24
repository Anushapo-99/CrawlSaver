"""
Example script demonstrating CrawlSaver integration with Selenium
for scraping a paginated website with resume capability.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from webdriver_manager.chrome import ChromeDriverManager

# Import CrawlSaver
from CrawlSaver import CrawlSaver

def main():
    # Initialize CrawlSaver
    saver = CrawlSaver("selenium_checkpoint.txt")
    
    # Try to load previous checkpoint
    checkpoint = saver.load_checkpoint()
    start_page = 1
    
    # If checkpoint exists, ask user if they want to resume
    if checkpoint:
        if saver.prompt_resume():
            start_page = checkpoint["page"]
            print(f"Resuming from page {start_page}")
        else:
            # User chose not to resume, so clear the checkpoint
            saver.clear_checkpoint()
    
    # Set up the webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Sample website with pagination (example: a hypothetical book listing site)
        base_url = "https://books.toscrape.com/catalogue/page-{}.html"
        
        # Scrape data starting from the page in the checkpoint (or page 1)
        current_page = start_page
        max_pages = 5  # Set a limit for this example
        
        while current_page <= max_pages:
            url = base_url.format(current_page)
            print(f"Scraping page {current_page}: {url}")
            
            # Navigate to the page
            driver.get(url)
            
            # Wait for the content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_pod"))
            )
            
            # Extract book titles as an example
            books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod h3 a")
            print(f"Found {len(books)} books on page {current_page}")
            
            for i, book in enumerate(books):
                title = book.get_attribute("title")
                print(f"  {i+1}. {title}")
            
            # Save checkpoint after processing this page
            checkpoint_data = {
                "page": current_page,
                "url": url,
                "timestamp": time.time()
            }
            saver.save_checkpoint(checkpoint_data)
            print(f"✅ Saved checkpoint for page {current_page}")
            
            # Simulate potential interruption (for demonstration purposes)
            if current_page == 3 and random.random() < 0.5:
                print("\n⚠️ Simulating a random interruption! The script will exit.")
                print("Run the script again to see how it can resume from the checkpoint.\n")
                break
            
            # Add a delay to be respectful to the website
            time.sleep(2)
            
            # Move to the next page
            current_page += 1
        
        print("Scraping completed successfully!")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("You can resume from the last checkpoint when you run the script again.")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()