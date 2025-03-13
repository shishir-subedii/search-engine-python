import requests
import time
import csv
import random
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 🔥 CONFIGURATION 🔥
CSV_FILE = "crawled_data.csv"

# 🌱 Seed URLs
seed_urls = [
    "https://en.wikipedia.org/wiki/Main_Page",
    "https://www.nytimes.com/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 🛠 Get last crawled URL from CSV
def get_last_crawled_url():
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:  # Check if there are data rows
                return reader[-1][0]  # Last URL column
    return None

# 🛠 Save extracted data to CSV file
def save_to_csv(data):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([data["url"], data["title"], data["description"]])

# 🔍 Extract metadata (title, description) from a page
def extract_metadata(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"❌ Skipping {url} - Status Code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        meta_tag = soup.find("meta", attrs={"name": "description"})
        description = meta_tag["content"].strip() if meta_tag else "No Description"

        return {"url": url, "title": title, "description": description}

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

# 🔍 Extract new links from a page
def extract_links(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(url, link["href"])
            parsed_url = urlparse(absolute_url)

            if parsed_url.scheme in {"http", "https"}:
                links.add(absolute_url)

        print(f"🔗 Found {len(links)} new links on {url}")
        return list(links)

    except Exception as e:
        print(f"❌ Error extracting links from {url}: {e}")
        return []

# 🕵️‍♂️ The Main Crawler Function
def crawl(starting_urls):
    to_crawl = []

    # 🔄 Resume from last crawled URL
    last_crawled = get_last_crawled_url()
    if last_crawled:
        print(f"\n⚠ Resuming from last crawled URL: {last_crawled}")
        to_crawl.append(last_crawled)
    else:
        to_crawl = starting_urls

    visited_urls = set()

    while to_crawl:
        url = to_crawl.pop(0)

        if url in visited_urls:
            continue

        print(f"🔍 Crawling: {url}")
        visited_urls.add(url)

        metadata = extract_metadata(url)
        if metadata:
            save_to_csv(metadata)
            print(f"✅ Saved: {metadata['title']} ({url})")

        new_links = extract_links(url)
        to_crawl.extend(new_links)

        time.sleep(random.uniform(1, 3))  # Small delay to avoid rate-limiting

# 🔄 Initialize CSV file if not already present
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "Meta Description"])

# 🚀 Run the Crawler
if __name__ == "__main__":
    try:
        crawl(seed_urls)
    except KeyboardInterrupt:
        print("\n🚪 Exiting... Progress saved.")
        #Works
