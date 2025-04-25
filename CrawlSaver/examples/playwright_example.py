"""
Example script demonstrating CrawlSaver integration with Playwright
for scraping a paginated website with resume capability.
"""
# This script uses Playwright to scrape book data from a paginated website.
import asyncio
from playwright.async_api import async_playwright
from CrawlSaver import CrawlSaver
import json
import time
import os


async def main():
    # Initialize CrawlSaver
    saver = CrawlSaver("playwright_checkpoint.txt")
    
    # Load checkpoint if it exists
    checkpoint = saver.load_checkpoint()
    start_page = 1
    
    # If checkpoint exists, ask user if they want to resume
    if checkpoint:
        if saver.prompt_resume():
            start_page = checkpoint.get("page", 1)
            print(f"Resuming from page {start_page}")
        else:
            # User chose not to resume, so clear the checkpoint
            saver.clear_checkpoint()
    
    # Ensure output directory exists
    os.makedirs("playwright_output", exist_ok=True)
    output_file = "playwright_output/book_data.json"
    
    # Initialize data list, loading existing data if resuming
    all_books = []
    if os.path.exists(output_file) and start_page > 1:
        try:
            with open(output_file, 'r') as f:
                all_books = json.load(f)
            print(f"Loaded {len(all_books)} existing books from output file")
        except json.JSONDecodeError:
            print("Error loading existing data, starting with empty dataset")
    
    # Initialize Playwright
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Configure max pages to scrape (for demo purposes)
        max_pages = 5
        current_page = start_page
        
        try:
            while current_page <= max_pages:
                url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"
                print(f"Scraping page {current_page}: {url}")
                
                # Navigate to the page
                await page.goto(url)
                
                # Wait for content to load
                await page.wait_for_selector("article.product_pod")
                
                # Extract book data using Python instead of JavaScript evaluation
                book_elements = await page.query_selector_all("article.product_pod")
                books = []
                
                for book_element in book_elements:
                    title_element = await book_element.query_selector("h3 a")
                    price_element = await book_element.query_selector("p.price_color")
                    availability_element = await book_element.query_selector("p.availability")
                    image_element = await book_element.query_selector("img")
                    
                    title = await title_element.get_attribute("title") if title_element else "Unknown"
                    price = await price_element.inner_text() if price_element else "Unknown"
                    
                    availability_text = "Unknown"
                    if availability_element:
                        availability_text = await availability_element.inner_text()
                        availability_text = availability_text.strip()
                    
                    image_src = await image_element.get_attribute("src") if image_element else None
                    
                    books.append({
                        "title": title,
                        "price": price,
                        "availability": availability_text,
                        "image": image_src,
                        "page": current_page
                    })
                
                print(f"Found {len(books)} books on page {current_page}")
                
                # Add books to our collection
                all_books.extend(books)
                
                # Save data to file after each page
                with open(output_file, 'w') as f:
                    json.dump(all_books, f, indent=2)
                
                # Save checkpoint after processing this page
                checkpoint_data = {
                    "page": current_page,
                    "url": url,
                    "books_collected": len(all_books),
                    "timestamp": time.time()
                }
                saver.save_checkpoint(checkpoint_data)
                print(f"✅ Saved checkpoint for page {current_page}")
                
                # Check if there's a next page
                has_next = await page.query_selector("li.next")
                if not has_next or current_page >= max_pages:
                    print("Reached the last page or maximum pages limit.")
                    break
                
                # Add a delay to be respectful to the website
                await asyncio.sleep(2)
                
                # Move to the next page
                current_page += 1
            
            print(f"Scraping completed! Collected data for {len(all_books)} books.")
            
            # Clear checkpoint after successful completion
            saver.clear_checkpoint()
            print("Checkpoint cleared as scraping completed successfully.")
        
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("You can resume from the last checkpoint when you run the script again.")
        
        finally:
            # Close the browser
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())