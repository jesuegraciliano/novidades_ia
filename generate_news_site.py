import os
from datetime import datetime
from scrape_openai import scrape_openai_news
from scrape_harvard import scrape_harvard_news
from scrape_google_news import scrape_google_news
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"

def resumir_titulo_em_portugues(titulo: str, fonte: str) -> str:
    prompt = f"Traduza para o português e escreva um breve resumo (3 frases) sobre esta manchete:\n\n{titulo}"
    resposta = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return resposta.choices[0].message.content.strip()

def gerar_html(noticias: list[dict]) -> str:
    html = [
        "<!DOCTYPE html>",
        "<html lang='pt-BR'><head><meta charset='UTF-8'>",
        "<title>Resumo Diário de IA</title>",
        "<style>body{font-family:sans-serif;margin:2em;}li{margin-bottom:1.5em;}</style>",
        "</head><body>",
        f"<h1>🧠 Resumo Diário de Notícias sobre IA</h1>",
        f"<p>Atualizado em {datetime.now().strftime('%d/%m/%Y')}</p>",
        "<ul>"
    ]

    for n in noticias:
        html.append("<li>")
        html.append(f"<strong>{n['resumo']}</strong><br>")
        html.append(f"<a href='{n['url']}'>{n['title']}</a><br>")
        html.append(f"<em>Fonte: {n['source']}</em>")
        html.append("</li>")

    html.append("</ul><p style='font-size:0.8em;color:#999;'>Gerado com Python + OpenAI</p></body></html>")
    return "\n".join(html)

def main():
    print("📡 Coletando notícias...")
    noticias = (
        scrape_openai_news() +
        scrape_harvard_news() +
        scrape_google_news()
    )

    print(f"🔎 Resumindo {len(noticias)} manchetes...")
    for n in noticias:
        n["resumo"] = resumir_titulo_em_portugues(n["title"], n["source"])

    print("📝 Gerando HTML...")
    conteudo_html = gerar_html(noticias)

    os.makedirs("site", exist_ok=True)
    with open("site/index.html", "w", encoding="utf-8") as f:
        f.write(conteudo_html)

    print("✅ site/index.html gerado com sucesso.")

if __name__ == "__main__":
    main()
