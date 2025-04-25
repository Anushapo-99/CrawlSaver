from CrawlSaver.checkpoint import CrawlSaver
from .integrations.requests import RequestsSaver
from .integrations.playwright import PlaywrightSaver
from .integrations.scrapy import ScrapySaver
from .integrations.selenium import SeleniumSaver

__all__ = ["CrawlSaver", "SQLiteSaver", "RequestsSaver", "PlaywrightSaver", "ScrapySaver", "SeleniumSaver"]


"**CrawlSaver**"

"""
    Base class for saving and resuming web crawling progress.
    
    CrawlSaver provides a framework for checkpoint management during web scraping
    operations, allowing graceful recovery from interruptions by storing the crawl
    state and resuming from the last successful point.
    
    Attributes:
        checkpoint_path (str): Path to store checkpoint data
        auto_save (bool): Whether to automatically save checkpoints after each request
        batch_size (int): Number of requests to process before saving a checkpoint when auto_save is True
    
    Methods:
        save_checkpoint(): Saves the current crawl state
        load_checkpoint(): Loads the previously saved crawl state
        clear_checkpoint(): Removes the saved checkpoint data
        is_visited(url): Checks if a URL has already been processed
        mark_visited(url): Marks a URL as processed
        get_next_url(): Returns the next URL to process
        add_urls(urls): Adds new URLs to the crawl queue
    """



"RequestsSaver"

"""
    CrawlSaver implementation for the Python Requests library.
    
    Provides checkpoint functionality specifically tailored for web crawlers
    built with the Requests HTTP library.
    
    Attributes:
        session (requests.Session): The requests session to track and save
        headers (dict): Default headers to use for requests
        cookies (dict): Cookies to maintain between requests
        
    Methods:
        get(url, **kwargs): Wraps requests.get with checkpoint functionality
        post(url, **kwargs): Wraps requests.post with checkpoint functionality
        save_response(response, filename): Saves response content to file
        restore_session(): Restores session cookies and headers from checkpoint
        
    Usage example:
        ```python
        saver = RequestsSaver("checkpoints/my_crawl")
        response = saver.get("https://example.com")
        saver.save_checkpoint()
        ```
    """

"PlaywrightSaver"

"""
    CrawlSaver implementation for the Playwright automation library.
    
    Provides checkpoint functionality for browser automation scripts using
    Playwright, supporting Chromium, Firefox, and WebKit browsers.
    
    Attributes:
        browser (playwright.Browser): The browser instance being used
        context (playwright.BrowserContext): The current browser context
        storage_state (dict): Saved cookies and localStorage data
        
    Methods:
        new_page(): Creates a new page with checkpoint tracking
        goto(url, **kwargs): Navigates to URL with checkpoint awareness
        take_screenshot(selector, filename): Takes a screenshot and saves it
        save_storage_state(path): Saves cookies and storage for later resumption
        load_storage_state(path): Loads previously saved browser state
        
    Usage example:
        ```python
        saver = PlaywrightSaver("checkpoints/playwright_crawl")
        page = saver.new_page()
        await page.goto("https://example.com")
        saver.save_checkpoint()
        ```
    """

"ScrapySaver"

"""
    CrawlSaver implementation for the Scrapy web crawling framework.
    
    Integrates with Scrapy's architecture to provide checkpoint functionality
    through spider middleware and extensions.
    
    Attributes:
        spider (scrapy.Spider): Reference to the current spider
        stats (scrapy.statscollectors.StatsCollector): Scrapy stats collector
        settings (scrapy.settings.Settings): Scrapy settings object
        
    Methods:
        from_crawler(cls, crawler): Creates ScrapySaver from crawler
        process_request(request): Processes and tracks outgoing requests
        process_response(response): Processes and tracks incoming responses
        process_spider_output(result): Processes items and requests from callbacks
        resume_requests(): Returns requests to retry from checkpoint
        
    Usage example:
        ```python
        # In spider's __init__ method:
        self.saver = ScrapySaver("checkpoints/scrapy_crawl")
        
        # In spider middleware:
        def process_spider_output(self, response, result, spider):
            return self.saver.process_spider_output(result)
        ```
    """

"SeleniumSaver"

"""
    CrawlSaver implementation for the Selenium WebDriver.
    
    Provides checkpoint functionality for browser automation scripts using
    Selenium WebDriver, supporting various browsers through their drivers.
    
    Attributes:
        driver (selenium.webdriver.Remote): The WebDriver instance
        wait_time (int): Default time to wait for elements in seconds
        
    Methods:
        get(url): Navigates to URL with checkpoint awareness
        save_cookies(filename): Saves current cookies to file
        load_cookies(filename): Loads cookies from file
        find_element_safe(by, value): Finds element with error handling
        screenshot(filename): Takes a screenshot of the current page
        execute_with_retry(command, *args): Executes commands with retry logic
        
    Usage example:
        ```python
        driver = webdriver.Chrome()
        saver = SeleniumSaver("checkpoints/selenium_crawl", driver=driver)
        saver.get("https://example.com")
        saver.save_checkpoint()
        ```
    """




