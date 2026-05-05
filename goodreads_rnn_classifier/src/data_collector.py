import time
import pandas as pd
from bs4 import BeautifulSoup
from requests import get

BASE_URL = "https://www.goodreads.com"

HDR = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}


def fetch_book_description(url):
    """
    Fetch ONLY description (used in API)
    """
    try:
        response = get(url, headers=HDR, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        desc_block = soup.find("div", {"class": "readable stacked"})
        if not desc_block:
            return None

        spans = desc_block.find_all("span")
        if not spans:
            return None

        return spans[-1].text.strip()

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return None


def collect_book_urls(list_url, start_page=1, end_page=5, delay=2):
    """
    Scrape Goodreads list pages and extract book URLs
    """
    urls = []

    for page in range(start_page, end_page + 1):
        print(f"Reading page {page}")
        response = get(f"{list_url}?page={page}", headers=HDR)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table", {"class": "tableList"})
        if not table:
            continue

        rows = table.find_all("tr")

        for r in rows:
            link = r.find("a", {"class": "bookTitle"})
            if link:
                urls.append(BASE_URL + link["href"])

        time.sleep(delay)

    return urls


def fetch_book_data(url):
    """
    Full scraper (used for dataset building)
    """
    try:
        response = get(url, headers=HDR, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        book = {}

        # Title
        title = soup.find("h1", {"id": "bookTitle"})
        book["book_title"] = title.text.strip() if title else ""

        # Description
        desc_block = soup.find("div", {"class": "readable stacked"})
        if desc_block:
            spans = desc_block.find_all("span")
            book["book_desc"] = spans[-1].text.strip() if spans else ""
        else:
            book["book_desc"] = ""

        # Genres
        genres = soup.find_all("a", {"class": "bookPageGenreLink"})
        book["genres"] = "|".join([g.text for g in genres])

        return book

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return None


def build_dataset(list_url, start_page=1, end_page=5, save_path="data/books.csv"):
    """
    Full pipeline: URLs -> book data -> CSV
    """
    urls = collect_book_urls(list_url, start_page, end_page)

    data = []
    for i, url in enumerate(urls):
        print(f"Scraping {i+1}/{len(urls)}")

        book = fetch_book_data(url)
        if book:
            data.append(book)

        time.sleep(2)

    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False)

    print(f"Saved dataset to {save_path}")
