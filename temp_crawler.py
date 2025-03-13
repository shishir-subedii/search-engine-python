#(not recommended)this uses .txt file to store the data and resume from the last crawled URL
import requests
import time
import csv
import random
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# 🔥 CONFIGURATION 🔥
CSV_FILE = "crawled_data.csv"
VISITED_FILE = "visited_urls.txt"

# 🌱 Seed URLs
seed_urls = [
    "https://en.wikipedia.org/wiki/Main_Page",
    "https://www.nytimes.com/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 🛠 Load previously visited URLs
def load_visited_urls():
    if os.path.exists(VISITED_FILE):
        with open(VISITED_FILE, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    return set()

# 🛠 Save visited URLs to file
def save_visited_url(url):
    with open(VISITED_FILE, "a", encoding="utf-8") as file:
        file.write(url + "\n")

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
def extract_links(url, visited_urls):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(url, link["href"])
            parsed_url = urlparse(absolute_url)

            if parsed_url.scheme in {"http", "https"} and absolute_url not in visited_urls:
                links.add(absolute_url)

        print(f"🔗 Found {len(links)} new links on {url}")
        return list(links)

    except Exception as e:
        print(f"❌ Error extracting links from {url}: {e}")
        return []

# 🕵️‍♂️ The Main Crawler Function
def crawl(starting_urls):
    visited_urls = load_visited_urls()
    to_crawl = [url for url in starting_urls if url not in visited_urls]

    while True:  # 🔄 Infinite loop for continuous crawling
        if not to_crawl:
            print("\n⚠ All seed URLs have been visited. Continuing from the last crawled link...")

            last_visited = None
            if os.path.exists(VISITED_FILE):
                with open(VISITED_FILE, "r", encoding="utf-8") as file:
                    lines = file.read().splitlines()
                    if lines:
                        last_visited = lines[-1]  # Get the last visited URL

            if last_visited and last_visited not in visited_urls:
                to_crawl.append(last_visited)
                print(f"🔄 Resuming from: {last_visited}")
            else:
                print("🔍 Extracting new links from last visited URL...")
                new_links = extract_links(last_visited, visited_urls)

                if new_links:
                    to_crawl.extend(new_links)
                    print(f"✅ Added {len(new_links)} new links to crawl queue.")
                else:
                    print("✅ No more links found. Waiting for new pages...")
                    time.sleep(5)  # 🔄 Pause before retrying

        url = to_crawl.pop(0)

        if url in visited_urls:
            continue

        print(f"🔍 Crawling: {url}")
        visited_urls.add(url)
        save_visited_url(url)

        metadata = extract_metadata(url)
        if metadata:
            save_to_csv(metadata)
            print(f"✅ Saved: {metadata['title']} ({url})")

        new_links = extract_links(url, visited_urls)
        to_crawl.extend(new_links)

        time.sleep(random.uniform(1, 3))  # ⏳ Avoid rate-limiting

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
        #done
