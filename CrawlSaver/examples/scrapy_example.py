"""
Scrapy spider example with CrawlSaver integration

This demonstrates how to use CrawlSaver to save and resume Scrapy crawls.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from CrawlSaver import CrawlSaver
import os
import json


class BookSpider(scrapy.Spider):
    name = "books"
    
    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        # Initialize CrawlSaver
        self.saver = CrawlSaver("scrapy_checkpoint.txt")
        
        # Load checkpoint if it exists
        self.checkpoint = self.saver.load_checkpoint()
        self.start_page = 1
        
        # If checkpoint exists and user wants to resume
        if self.checkpoint and self.saver.prompt_resume():
            self.start_page = self.checkpoint.get("last_page", 1)
            self.logger.info(f"Resuming from page {self.start_page}")
        else:
            # Clear checkpoint if not resuming
            self.saver.clear_checkpoint()
        
        # Set the starting URL based on the checkpoint
        self.start_urls = [f"https://books.toscrape.com/catalogue/page-{self.start_page}.html"]
        
        # Keep track of processed items
        self.items_processed = 0
        self.current_page = self.start_page
        self.max_pages = 5  # Limit for demo purposes

    def parse(self, response):
        # Extract book information
        books = response.css("article.product_pod")
        
        for book in books:
            title = book.css("h3 a::attr(title)").get()
            price = book.css("p.price_color::text").get()
            availability = book.css("p.availability::text").get()
            
            self.items_processed += 1
            
            yield {
                "title": title,
                "price": price,
                "availability": availability,
                "page": self.current_page
            }
        
        self.logger.info(f"Processed {len(books)} books on page {self.current_page}")
        
        # Save checkpoint after processing this page
        checkpoint_data = {
            "last_page": self.current_page,
            "items_processed": self.items_processed,
            "last_url": response.url
        }
        self.saver.save_checkpoint(checkpoint_data)
        self.logger.info(f"Saved checkpoint for page {self.current_page}")
        
        # Check for next page and follow if within limits
        next_page = response.css("li.next a::attr(href)").get()
        if next_page and self.current_page < self.max_pages:
            self.current_page += 1
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info("Crawl completed successfully!")


# Function to run the spider
def run_spider():
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Configure settings for the Crawler
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output/books.json": {"format": "json", "overwrite": False},
        },
        "LOG_LEVEL": "INFO",
        # Be respectful with scraping speed
        "DOWNLOAD_DELAY": 1,
    })
    
    # Start the crawler
    process.crawl(BookSpider)
    process.start()


if __name__ == "__main__":
    run_spider()