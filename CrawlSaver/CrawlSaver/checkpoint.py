"""
    CrawlSaver - A library for managing web scraping interruptions."""
import os
import json

class CrawlSaver:
    """
    CrawlSaver - A library for managing web scraping interruptions.
    
    This class provides functionality to save, load, and clear checkpoints
    during web scraping operations. It allows scraping processes to be 
    resumed from where they left off after interruptions.
    
    Checkpoints are stored as JSON data in text files for easy reading
    and modification if needed.
    
    Attributes:
        checkpoint_file (str): Path to the file where checkpoint data is stored.
                               Defaults to "checkpoint.txt" in the current directory.
    
    Example:
        >>> saver = CrawlSaver("my_scraper_checkpoint.txt")
        >>> # Save progress after processing a page
        >>> saver.save_checkpoint({"page": 5, "url": "https://example.com/page/5"})
        >>> # Later, load the checkpoint to resume
        >>> checkpoint = saver.load_checkpoint()
        >>> if checkpoint and saver.prompt_resume():
        >>>     start_page = checkpoint["page"]
        >>> else:
        >>>     start_page = 1
    """
    
    def __init__(self, checkpoint_file="checkpoint.txt"):

        """
        Initialize a new CrawlSaver instance.
        
        Args:
            checkpoint_file (str, optional): Path to the file where checkpoint 
                                            data will be stored. Defaults to 
                                            "checkpoint.txt" in the current directory.
        """

        self.checkpoint_file = checkpoint_file
    
    def save_checkpoint(self, data):
        """
        Save checkpoint data to a file.
        
        The data is serialized as JSON and written to the checkpoint file.
        Any existing checkpoint data will be overwritten.
        
        Args:
            data (dict): The checkpoint data to save. Can be any JSON-serializable 
                        Python object (typically a dictionary containing scraping progress).
        
        Returns:
            None
            
        Raises:
            IOError: If the file cannot be written to.
            TypeError: If the data cannot be serialized to JSON.
        """

        with open(self.checkpoint_file, 'w') as f:
            json.dump(data, f)
    
    def load_checkpoint(self):

        """
        Load checkpoint data from a file.
        
        Reads and deserializes JSON data from the checkpoint file.
        
        Returns:
            dict or None: The checkpoint data if the file exists and contains valid JSON,
                         or None if the file doesn't exist or is empty.
                         
        Raises:
            json.JSONDecodeError: If the file contains invalid JSON.
            IOError: If the file exists but cannot be read.
        """

        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return None
    
    def clear_checkpoint(self):
        
        """
        Clear stored checkpoint by removing the checkpoint file.
        
        This method deletes the checkpoint file if it exists,
        effectively resetting the scraping progress.
        
        Returns:
            None
            
        Raises:
            OSError: If the file exists but cannot be removed.
        """

        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
    
    def prompt_resume(self):

        """
        Prompt the user to decide whether to resume from the last checkpoint.
        
        This interactive method asks the user whether they want to resume 
        the scraping process from where it left off or start from the beginning.
        
        Returns:
            bool: True if the user wants to resume, False otherwise.
            
        Note:
            This method will continue prompting until a valid response is given.
            Valid responses are 'y', 'yes', 'n', or 'no' (case-insensitive).
        """
        checkpoint = self.load_checkpoint()
        scraped = checkpoint.get("scraped", 0) if checkpoint else 0
        total = checkpoint.get("total", "unknown") if checkpoint else "unknown"
        
        while True:
            response = input("📊 You have already scraped {scraped} out of {total} URLs. "
                         "Do you want to resume (y) or start from beginning (n)? ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ Resuming from last checkpoint.")
                return True
            elif response in ['n', 'no']:
                print("🔁 Starting from beginning.")
                return False
            else:
                print("❓ Please enter 'y' or 'n'.")
       

