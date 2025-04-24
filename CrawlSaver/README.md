# CrawlSaver - Web Scraping Progress Tracker

CrawlSaver is a lightweight Python library that helps web scrapers automatically track and resume progress after interruptions without manual checkpoint management. It supports multiple web scraping frameworks, including Requests, Playwright, Scrapy, and Selenium.It eliminates the need to hardcode checkpoints (like last_page = 0) and instead automatically saves and restores scraping progress across interruptions (crashes, network failures, or script restarts).

**Features**

Automatic Progress Tracking: Save scraping progress dynamically.

Checkpoint Management: Resume from the last saved URL, page number, or ID.

Flexible Storage Options: Supports text files and (upcoming) SQLite.

Multi-framework Integration: Works with Requests, Playwright, Scrapy, and Selenium.

User Control: Choose to resume from a checkpoint or start fresh.

Easy to Use: Simple API for seamless integration.

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

SQLite	      |  Coming Soon	  |   More scalable for large projects.


**🛠 Supported Frameworks**

Framework	Status	Helper Functions
Requests	✅ Supported	for_requests(), mark_processed_in_requests()
Playwright	✅ Supported	for_playwright(), mark_processed_in_playwright()
Selenium	🔜 Coming Soon	(Work in progress)
Scrapy	🔜 Coming Soon	(Middleware integration planned)



**🔮 Future Roadmap**

    ✅ SQLite Support – For larger-scale scraping projects.

    ✅ Selenium & Scrapy Integration – Native helpers for these frameworks.

    ✅ Distributed Scraping Support – Multi-machine checkpointing.

    ✅ Custom Serialization – Support for custom data formats.

    
**💡 Who Should Use This?**

✔ Web scrapers who want automatic failure recovery.

✔ Data engineers managing long-running scraping jobs.

✔ Researchers collecting large datasets without manual checkpointing.