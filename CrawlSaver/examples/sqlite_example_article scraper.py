
# This script scrapes article titles and authors from a newspaper website.
# It uses SQLite to store URLs and a JSON file to save scraped data.
# The script resumes from the last scraped URL using a checkpoint manager.
import os
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from CrawlSaver import SQLiteSaver

# -- Setup --
DB_PATH = "/home/anusha/Desktop/DATAHUT/CrawlSaver/CrawlSaver/examples/articles_url.db"
TABLE_NAME = "url"
DATA_TABLE = "data"
JSON_FILE = "/home/anusha/Desktop/DATAHUT/CrawlSaver/CrawlSaver/examples/thehindu_articles.json"

# Load existing JSON data if any
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        scraped_data = json.load(f)
        scraped_urls = set(entry["url"] for entry in scraped_data if "url" in entry)
else:
    scraped_data = []
    scraped_urls = set()

# -- Scraper function --
def extract_article_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.select_one('h1.title[itemprop="name"]')
        author = soup.select_one('div.author-name a.person-name')

        return {
            "url": url,
            "title": title.get_text(strip=True) if title else None,
            "author": author.get_text(strip=True) if author else None
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

# -- Main Workflow --
def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create target data table if not exists
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DATA_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            author TEXT
        )
    """)
    conn.commit()

    # Load all URLs
    cursor.execute(f"SELECT rowid, url FROM {TABLE_NAME}")
    all_urls = cursor.fetchall()

    # Use SQLiteSaver checkpoint manager
    saver = SQLiteSaver(DB_PATH)
    resume = saver.prompt_resume()
    last_id = saver.load_last_id() if resume else 0

    print(f"🚀 Starting scraping from rowid {last_id + 1}")

    for rowid, url in all_urls:
        if rowid <= last_id:
            continue
        if url in scraped_urls:
            print(f"⏭️ Skipping already scraped URL: {url}")
            saver.save_last_id(rowid)
            continue

        print(f"🔎 Scraping rowid={rowid} | URL={url}")
        article = extract_article_data(url)
        if article:
            # Save to JSON
            scraped_data.append(article)
            scraped_urls.add(url)
            with open(JSON_FILE, "w") as jf:
                json.dump(scraped_data, jf, indent=2)

            # Save to SQLite database
            try:
                cursor.execute(f"""
                    INSERT OR IGNORE INTO {DATA_TABLE} (url, title, author)
                    VALUES (?, ?, ?)
                """, (article["url"], article["title"], article["author"]))
                conn.commit()
            except Exception as e:
                print(f"❌ Error inserting into DB for {url}: {e}")

        # Update checkpoint
        saver.save_last_id(rowid)

    conn.close()
    print("✅ Done scraping all URLs.")

if __name__ == "__main__":
    main()
