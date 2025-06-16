#!/usr/bin/env python3
"""
Script unificado de scraping de notícias sobre IA,
resumo com OpenAI (10 linhas em português), e geração de site HTML.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"
MAX_PER_SITE = 3

def summarize_text(text: str) -> str:
    prompt = (
        f"Escreva um resumo em português com até 10 linhas, "
        f"claro e objetivo, sobre a seguinte manchete:\n\n{text}"
    )
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return resp.choices[0].message.content.strip()

def fetch_harvard():
    url = "https://news.harvard.edu/gazette/"
    soup = BeautifulSoup(requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text, "html.parser")
    return [{"title": a.get_text(strip=True), "url": a["href"], "source": "Harvard Gazette"}
            for a in soup.select("article h2.entry-title a")[:MAX_PER_SITE]]

def fetch_google_ai():
    url = "https://news.google.com/search?q=Artificial%20Intelligence&hl=en-US&gl=US&ceid=US:en"
    soup = BeautifulSoup(requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text, "html.parser")
    items = []
    for a in soup.select("a.DY5T1d")[:MAX_PER_SITE]:
        link = a["href"]
        if link.startswith("./"):
            link = "https://news.google.com" + link[1:]
        items.append({"title": a.get_text(strip=True), "url": link, "source": "Google News (AI)"})
    return items

def fetch_g1_ai():
    url = "https://g1.globo.com/tudo-sobre/inteligencia-artificial/"
    soup = BeautifulSoup(requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text, "html.parser")
    return [{"title": a.get_text(strip=True), "url": a["href"], "source": "G1 AI"}
            for a in soup.select("a.feed-post-link")[:MAX_PER_SITE]]

def fetch_cnn_tech():
    url = "https://www.cnnbrasil.com.br/tecnologia/"
    soup = BeautifulSoup(requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text, "html.parser")
    return [{"title": a.get_text(strip=True), "url": a["href"], "source": "CNN Brasil Tech"}
            for a in soup.select("h2.title a")[:MAX_PER_SITE]]

def fetch_folha_tech():
    url = "https://www1.folha.uol.com.br/tec/"
    soup = BeautifulSoup(requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).text, "html.parser")
    return [{"title": a.get_text(strip=True), "url": a["href"], "source": "Folha Tec"}
            for a in soup.select("div.tec--list__info a")[:MAX_PER_SITE]]

def generate_html(news):
    today = datetime.now().strftime("%d/%m/%Y")
    parts = [
        "<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>Resumo Diário IA</title>",
        "<style>body{font-family:sans-serif;margin:2em;}li{margin-bottom:1.5em;}</style></head><body>",
        f"<h1>🧠 Resumo Diário de Notícias sobre IA — {today}</h1><ul>"
    ]
    for item in news:
        parts.append("<li>")
        parts.append(f"<a href='{item['url']}'><strong>{item['title']}</strong></a><br>")
        parts.append(f"<em>{item['source']}</em><p>{item['summary'].replace(chr(10),'<br>')}</p>")
        parts.append("</li>")
    parts.append("</ul><p style='font-size:0.8em;color:#666;'>Gerado com Python + OpenAI</p></body></html>")
    return "\n".join(parts)

def main():
    sources = [
        fetch_harvard, fetch_google_ai,
        fetch_g1_ai, fetch_cnn_tech, fetch_folha_tech
    ]

    all_news = []
    for fetch in sources:
        try:
            entries = fetch()
            print(f"✅ Coletados {len(entries)} de {fetch.__name__}")
            all_news.extend(entries)
        except Exception as e:
            print(f"⚠️ Falha ao coletar de {fetch.__name__}: {e}")

    for item in all_news:
        try:
            print(f"🔍 Resumindo: {item['title']}")
            item["summary"] = summarize_text(item["title"])
        except Exception as e:
            print(f"⚠️ Erro no resumo da manchete '{item['title']}': {e}")
            item["summary"] = "Resumo indisponível."

    html = generate_html(all_news)
    os.makedirs("site", exist_ok=True)
    with open("site/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ site/index.html criado com sucesso.")

if __name__ == "__main__":
    main()
