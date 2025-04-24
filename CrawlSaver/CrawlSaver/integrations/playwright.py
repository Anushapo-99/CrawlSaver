# Integration for Playwright
from CrawlSaver.checkpoint import CrawlSaver  


class PlaywrightSaver(CrawlSaver):
    """
    A specialized checkpoint manager for Playwright-based web scraping operations.
    
    PlaywrightSaver extends the base CrawlSaver class to provide checkpoint functionality
    specifically designed for Playwright automation scripts. This class enables saving
    and resuming web crawling operations when using the Playwright library for browser
    automation across Chromium, Firefox, and WebKit browsers.
    
    The class maintains the current URL state, allowing scripts to resume from the last
    visited page in case of interruptions, crashes, or scheduled pauses in the crawling process.
    
    Attributes:
        Inherits all attributes from CrawlSaver base class

    
    Usage Notes:
        - Typically used within async functions since Playwright is an async library
        - Can be extended to save additional state information beyond just URLs
        - Works alongside Playwright's built-in state persistence mechanisms
        - Best used within try/except blocks to handle potential errors during crawling
            
        """
    def save_url(self, url):

        """
        Saves the current URL to the checkpoint storage.
        
        This method enables tracking the crawling progress by saving the current URL
        as a checkpoint. It wraps the URL in a dictionary before passing it to the
        parent class's save_checkpoint method.
        
        Args:
            url (str): The URL to save as the current checkpoint position.
            
        Returns:
            None
            
        Raises:
            TypeError: If the provided URL is not a string.
            ValueError: If the URL is empty or invalid.
        """
        self.save_checkpoint({"url": url})
    
    def load_url(self):

        """
        Retrieves the last saved URL from the checkpoint storage.
        
        This method loads the previously saved checkpoint and extracts the URL
        from it. If no checkpoint exists or the checkpoint doesn't contain a URL,
        it returns None.
        
        Args:
            None
            
        Returns:
            str or None: The last saved URL if available, None otherwise.
            
        Note:
            The returned URL can be directly used with Playwright's page.goto()
            method to resume crawling from the last position.
        """
        
        checkpoint = self.load_checkpoint()
        return checkpoint.get("url", None) if checkpoint else None
