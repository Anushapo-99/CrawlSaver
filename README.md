# CrawlSaver - Web Scraping Progress Tracker

CrawlSaver is a lightweight Python library that helps web scrapers automatically track and resume progress after interruptions without manual checkpoint management. It supports multiple web scraping frameworks, including Requests, Playwright, Scrapy, and Selenium.It eliminates the need to hardcode checkpoints (like last_page = 0) and instead automatically saves and restores scraping progress across interruptions (crashes, network failures, or script restarts).

**Features**

✅Automatic Progress Tracking: Save scraping progress dynamically.

✅Checkpoint Management: Resume from the last saved URL, page number, or ID.

✅Flexible Storage Options: Supports text files and SQLite.

✅Multi-framework Integration: Works with Requests, Playwright, Scrapy, and Selenium.

✅User Control: Choose to resume from a checkpoint or start fresh.

✅Easy to Use: Simple API for seamless integration.

**🚀 Why Use CrawlSaver?**

**Web scraping often fails due to:**

❌ Network errors (connection drops, rate limits)

❌ Script crashes (unexpected exceptions)

❌ Manual checkpoint management (tedious and error-prone)

**CrawlSaver solves these issues by:**

✅ Automatically tracking progress – No need to manually update last_page or last_url.

✅ Resuming from failures – If the script crashes, it continues where it left off.

✅ Supporting multiple frameworks – Works seamlessly with popular scraping tools.


**📂 Storage Options**
 
Storage Type	|   Status	      |      Description

JSON File	   |  Available	    |   Simple file-based storage (default).

SQLite	      |  Available	    |   More scalable for large projects.


**🛠 Supported Frameworks**

Framework	Status	Helper Functions
Requests	✅ Supported	for_requests(), mark_processed_in_requests()
Playwright	✅ Supported	for_playwright(), mark_processed_in_playwright()
Selenium	🔜 Coming Soon	(Work in progress)
Scrapy	🔜 Coming Soon	(Middleware integration planned)



**🔮 Future Roadmap**


Selenium & Scrapy Integration – Native helpers for these frameworks.

Distributed Scraping Support – Multi-machine checkpointing.

Custom Serialization – Support for custom data formats.




    
**💡 Who Should Use This?**

✔ Web scrapers who want automatic failure recovery.

✔ Data engineers managing long-running scraping jobs.

✔ Researchers collecting large datasets without manual checkpointing





**📝 Usage Example: Selenium Integration**

The example **"CrawlSaver/examples/selenium_example.py"** file demonstrates how to integrate CrawlSaver into a Selenium-based scraper for a paginated website (e.g., books.toscrape.com). This example shows how to:

   ✔ Resume from the last scraped page after an interruption

   ✔ Save progress after each page

   ✔ Use CrawlSaver's checkpointing with minimal code changes

   ✔ Run it once to start scraping.
   
   ✔ Interrupt it manually (or let the simulated interruption happen)
   
   ✔ Re-run the script to see it resume automatically from the last checkpoint


**🔍 How This Example Works**

1] Initialize CrawlSaver: Create a CrawlSaver instance with a specified checkpoint file.

    saver = CrawlSaver("selenium_checkpoint.txt")

2] Resume Logic: The script checks if a previous checkpoint exists and prompts the user to choose whether to resume or start fresh.
    
    checkpoint = saver.load_checkpoint()
    start_page = 1

    if checkpoint:
         if saver.prompt_resume():
             start_page = checkpoint["page"]
             
        
3] Selenium Setup: Configure and initialize the Chrome WebDriver with appropriate options.


4] Pagination Handling: The script works through multiple pages, saving a checkpoint after each completed page.

    checkpoint_data = {
                    "page": current_page,
                    "url": url,
                    "timestamp": time.time()
                }
                saver.save_checkpoint(checkpoint_data)


5] Interruption Recovery: When the script runs again after an interruption, it can resume from the last successfully processed page.


**📌 Key Benefits Demonstrated**

>Zero Progress Loss: If the script crashes or is interrupted, your progress is saved.

>Simple Integration: Just a few lines of code to add robust checkpointing.

>User Control: Option to resume or start fresh when a checkpoint exists.

>Graceful Error Handling: Even unexpected errors won't lose your scraping progress.

