# Integration for Scrapy

from CrawlSaver.checkpoint import CrawlSaver  


class ScrapySaver(CrawlSaver):

    """
    ScrapySaver - Specialized CrawlSaver implementation for the Scrapy web crawling framework.
    
    This class extends the base CrawlSaver to provide Scrapy-specific checkpoint functionality,
    allowing for the persistent tracking and resumption of web crawling operations in Scrapy
    projects. It enables saving and loading lists of scraped URLs, facilitating recovery from
    interruptions without duplicating work.
    
    Inherits from:
        CrawlSaver: Base checkpoint management class providing core functionality
                    for saving and restoring crawl state.
    
    Key Features:
        - Specialized URL tracking for Scrapy spiders
        - Persistence of scraped URL collections
        - Simple interface for Scrapy integration
        - Resumable crawls after interruption
    
        Attributes:
        Inherits all attributes from CrawlSaver parent class
    
    Methods:
        save_scraped_urls(urls): Saves a list of URLs that have been scraped
        load_scraped_urls(): Loads previously saved list of scraped URLs
    """

    def save_scraped_urls(self, urls):

        """
        Save a list of URLs that have been scraped to the checkpoint.
        
        This method wraps the base class save_checkpoint method to store
        the list of URLs in a standardized format. This makes it easy to
        track which URLs have already been processed, preventing duplicate
        work when resuming an interrupted crawl.
        
        Args:
            urls (list): List of URL strings that have been successfully scraped
                         and should not be revisited upon crawl resumption.
        
        Returns:
            None
        """
        self.save_checkpoint({"urls": urls})
    
    def load_scraped_urls(self):

        """
        Load the previously saved list of scraped URLs from the checkpoint.
        
        This method retrieves the list of URLs that were saved in a previous
        crawl session, allowing the spider to avoid reprocessing URLs that
        have already been handled.
        
        Returns:
            list: A list of URL strings that have been previously scraped,
                  or an empty list if no checkpoint data exists.
        """
        
        checkpoint = self.load_checkpoint()
        return checkpoint.get("urls", []) if checkpoint else []
