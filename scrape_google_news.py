import requests
from bs4 import BeautifulSoup
from typing import List

def scrape_google_news(max_items: int = 3) -> List[dict]:
    url = "https://news.google.com/home?hl=pt-BR&gl=BR&ceid=BR:pt-419"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    articles = soup.select("a.DY5T1d")

    for a in articles[:max_items]:
        title = a.get_text(strip=True)
        partial_link = a.get("href", "")
        full_url = "https://news.google.com" + partial_link[1:] if partial_link.startswith("./") else partial_link
        results.append({
            "title": title,
            "url": full_url,
            "source": "Google News"
        })

    return results
