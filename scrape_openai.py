import requests
from bs4 import BeautifulSoup
from typing import List

def scrape_openai_news(max_items: int = 3) -> List[dict]:
    url = "https://openai.com/news"
    headers = {"User-Agent": "IA-News-Scraper/1.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    articles = soup.select("a.py-3")  # links para posts

    for link in articles[:max_items]:
        href = link["href"]
        full_url = "https://openai.com" + href
        title = link.get_text(strip=True)
        results.append({
            "title": title,
            "url": full_url,
            "source": "OpenAI"
        })

    return results
