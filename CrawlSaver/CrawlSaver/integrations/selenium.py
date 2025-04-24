
# Integration for Selenium

from CrawlSaver.checkpoint import CrawlSaver  # Correct import


class SeleniumSaver(CrawlSaver):

    """
    CrawlSaver implementation specifically designed for Selenium WebDriver-based web scrapers.
    
    This class extends the base CrawlSaver to provide checkpoint functionality for
    Selenium automation scripts, allowing them to save their state and resume from
    the last successfully processed page if interrupted.
    
    The SeleniumSaver manages pagination state during crawls, storing the last processed
    page number and providing methods to retrieve this information when resuming a crawl.
    This is particularly useful for paginated content where tracking the current page
    is essential for resumption.
    
    Attributes:
        All attributes inherited from CrawlSaver base class
        
    """

    def save_last_page(self, page_number):

        """
        Save the current page number to the checkpoint.
        
        This method stores the current pagination state allowing the crawler
        to resume from this specific page if interrupted.
        
        Args:
            page_number (int): The current page number being processed
            
        Returns:
            None
            
        Note:
            This method calls the underlying save_checkpoint method from the
            CrawlSaver base class, storing the page number in a dictionary
            under the 'page' key.
        """

        self.save_checkpoint({"page": page_number})
    
    def load_last_page(self):

        """
        Retrieve the last saved page number from the checkpoint.
        
        This method is used when resuming a crawl to determine which page
        was last successfully processed.
        
        Args:
            None
            
        Returns:
            int: The last processed page number, or 1 if no checkpoint exists
                 or the 'page' key is not found in the checkpoint data
                 
        Note:
            If no checkpoint exists or the checkpoint doesn't contain page
            information, this method defaults to returning 1, assuming the
            crawl should start from the first page.
        """
        
        checkpoint = self.load_checkpoint()
        return checkpoint.get("page", 1) if checkpoint else 1
