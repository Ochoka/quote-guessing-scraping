import requests
from bs4 import BeautifulSoup
import json
import os
from time import sleep

BASE_URL = "http://quotes.toscrape.com"
CACHE_FILE = "quotes_cache.json"
BLOCK_SIZE = 10

def scrape_quotes(start_index=0):
    all_quotes = load_quotes_from_cache()
    scraped = []
    page = 1
    seen_texts = set(q["text"] for q in all_quotes)

    while len(scraped) < BLOCK_SIZE:
        try:
            response = requests.get(f"{BASE_URL}/page/{page}", timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        if not quotes:
            break

        for quote in quotes:
            text = quote.find(class_="text").get_text()
            if text in seen_texts:
                continue

            author = quote.find(class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_="tag")]
            bio_link = quote.find("a")["href"]
            author_info = get_author_bio(bio_link)

            scraped.append({
                "text": text,
                "author": author,
                "tags": tags,
                "bio-link": bio_link,
                "birth_date": author_info["birth_date"],
                "birth_place": author_info["birth_place"],
                "bio_description": author_info["bio_description"]
            })

            seen_texts.add(text)

            if len(scraped) + len(all_quotes) >= start_index + BLOCK_SIZE:
                break

        page += 1
        sleep(0.5)

    updated_quotes = all_quotes + scraped
    latest_block = updated_quotes[-BLOCK_SIZE:]
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(latest_block, f, ensure_ascii=False, indent=2)

    return latest_block

def get_author_bio(bio_url):
    response = requests.get(f"{BASE_URL}{bio_url}")
    soup = BeautifulSoup(response.text, "html.parser")
    birth_date = soup.find(class_="author-born-date").get_text()
    birth_place = soup.find(class_="author-born-location").get_text()
    bio = soup.find(class_="author-description").get_text().strip()

    return {
        "birth_date": birth_date,
        "birth_place": birth_place,
        "bio_description": bio
    }

def load_quotes_from_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
