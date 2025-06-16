import requests
from bs4 import BeautifulSoup
from typing import List

def scrape_harvard_news(max_items: int = 3) -> List[dict]:
    url = "https://news.harvard.edu/gazette/"
    headers = {"User-Agent": "IA-News-Scraper/1.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    articles = soup.select("article h2.entry-title a")

    for link in articles[:max_items]:
        title = link.get_text(strip=True)
        href = link["href"]
        results.append({
            "title": title,
            "url": href,
            "source": "Harvard Gazette"
        })

    return results
