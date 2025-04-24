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

        while True:
            response = input("📝 Do you want to resume from the last checkpoint? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ Resuming from last checkpoint.")
                return True
            elif response in ['n', 'no']:
                print("🔁 Starting from beginning.")
                return False
            else:
                print("❓ Please enter 'y' or 'n'.")
       



import sqlite3
import os

class SQLiteSaver:
    """
    SQLiteSaver - A SQLite-based checkpoint manager for web scraping operations.
    
    Automatically creates the checkpoint database and table if they don't exist.
    Tracks last processed ID to support scraping resume functionality.
    """

    def __init__(self, db_file="checkpoint.db"):
        """
        Initialize a new SQLiteSaver instance.

        Args:
            db_file (str): Path to the SQLite database file. Defaults to 'checkpoint.db'.
        """
        self.db_file = db_file
        self._ensure_db_and_table()

    def _ensure_db_and_table(self):
        """Ensure the checkpoint DB file and table exist."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS checkpoint (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_processed_id INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def save_last_id(self, last_id):
        """Save the last processed ID to the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoint")
        cursor.execute("INSERT INTO checkpoint (last_processed_id) VALUES (?)", (last_id,))
        conn.commit()
        conn.close()

    def load_last_id(self):
        """Load the last processed ID from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT last_processed_id FROM checkpoint ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

    def clear_checkpoint(self):
        """Clear all stored checkpoints from the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoint")
        conn.commit()
        conn.close()

    def prompt_resume(self):
        """Prompt the user to decide whether to resume from the last checkpoint."""
        while True:
            response = input("📝 Do you want to resume from the last checkpoint? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                print("✅ Resuming from last checkpoint.")
                return True
            elif response in ['n', 'no']:
                print("🔁 Starting from beginning.")
                return False
            else:
                print("❓ Please enter 'y' or 'n'.")



