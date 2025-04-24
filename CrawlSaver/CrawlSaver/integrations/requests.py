# Integration for Requests
from CrawlSaver.checkpoint import CrawlSaver  # Correct import


class RequestsSaver(CrawlSaver):
    """
    Checkpoint manager for Request-based web scrapers that handles pagination.
    
    The RequestsSaver extends the base CrawlSaver class to provide specialized
    functionality for saving and resuming crawls that involve paginated content.
    This implementation focuses on tracking the current page number in paginated
    websites, allowing crawls to resume from the exact page where they were
    interrupted.
    
    This class is particularly useful for scrapers that need to iterate through
    multiple pages of search results, listings, or other paginated content where
    maintaining the current page position is critical for resuming interrupted crawls.
    
    Attributes:
        Inherits all attributes from CrawlSaver base class
    
    Methods:
        save_page(page_number): Saves the current page number to the checkpoint
        load_page(): Retrieves the previously saved page number, defaulting to 1 if none exists
    """
    def save_page(self, page_number):
        """
        Saves the current page number to the checkpoint.
        
        This method wraps the parent class's save_checkpoint method to specifically
        save the current page number of a paginated crawl operation. It creates a
        dictionary with the page number and passes it to the underlying checkpoint
        mechanism.
        
        Args:
            page_number (int): The current page number to save
        
        Returns:
            None
        
        Raises:
            TypeError: If page_number is not an integer
            ValueError: If page_number is less than 1
        """
        
        self.save_checkpoint({"page": page_number})
    
    def load_page(self):

        """
        Retrieves the previously saved page number from the checkpoint.
        
        This method loads the checkpoint data and extracts the page number.
        If no checkpoint exists or the page number is not found in the
        checkpoint data, it returns 1 to start from the first page.
        
        Returns:
            int: The page number to resume from, defaulting to 1 if no
                 checkpoint exists
        
        Example:
            ```python
            saver = RequestsSaver("my_checkpoint")
            current_page = saver.load_page()
            print(f"Resuming from page {current_page}")
            ```
        """

        checkpoint = self.load_checkpoint()
        return checkpoint.get("page", 1) if checkpoint else 1