import requests
from time import sleep
from CrawlSaver.checkpoint import CrawlSaver  

# Initialize CrawlSaver with a custom checkpoint file
saver = CrawlSaver("requests_checkpoint.txt")

# Load the last checkpoint (if any)
checkpoint = saver.load_checkpoint()

# Ask user whether to resume or start fresh
if checkpoint and saver.prompt_resume():
    start_page = checkpoint.get("page", 1)
else:
    start_page = 1
    saver.clear_checkpoint()

# Example scraping loop
try:
    for page in range(start_page, 11):  # Simulate scraping pages 1 to 10
        print(f"📄 Scraping page {page}...")

        # Replace this with your actual scraping logic
        response = requests.get(f"https://httpbin.org/get?page={page}")
        data = response.json()

        # Simulate processing time
        sleep(1)

        # Save checkpoint after each successful page
        saver.save_checkpoint({"page": page})
        print(f"✅ Checkpoint saved at page {page}\n")

except KeyboardInterrupt:
    print("⚠️ Scraping interrupted. Progress saved.")
