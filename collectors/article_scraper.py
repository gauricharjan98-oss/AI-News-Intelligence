import requests
from bs4 import BeautifulSoup
from newspaper import Article


def extract_article_text(url):

    try:
        print(f"Extracting: {url}")

        article = Article(url)

        article.download()
        article.parse()

        text = article.text

        if text and len(text) > 200:
            print("Newspaper extraction successful")
            return text

        else:
            print("Newspaper extracted empty text")

    except Exception as e:
        print("Newspaper failed:", e)


    try:

        print("Trying BeautifulSoup fallback...")

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        paragraphs = soup.find_all("p")

        text = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
        )

        if text and len(text) > 200:
            print("BeautifulSoup extraction successful")
            return text


    except Exception as e:
        print("Scraper failed:", e)


    return None