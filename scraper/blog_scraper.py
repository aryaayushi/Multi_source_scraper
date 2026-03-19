import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json

from utils.helpers import detect_language
from utils.tagging import extract_keywords
from utils.chunking import chunk_text


def scrape_blog(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # ---------- Download page ----------
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

    except Exception as e:
        print(f"[REQUEST ERROR] {url}")
        return default_response(url)

    # ---------- Extract using newspaper ----------
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = article.text

    except:
        text = soup.get_text(separator=" ", strip=True)

    # ---------- AUTHOR ----------
    author = None

    try:
        author = ", ".join(article.authors) if article.authors else None
    except:
        pass

    # meta author
    if not author:
        meta_author = soup.find("meta", {"name": "author"})
        if meta_author:
            author = meta_author.get("content")

    # JSON-LD author
    if not author:
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)

                if isinstance(data, dict):
                    if "author" in data:
                        if isinstance(data["author"], dict):
                            author = data["author"].get("name")
                            break

            except:
                continue

    if not author:
        author = "Unknown Author"

    # ---------- DATE ----------
    published_date = None

    try:
        if article.publish_date:
            published_date = str(article.publish_date)
    except:
        pass

    # meta tags
    if not published_date:
        meta_tags = [
            {"property": "article:published_time"},
            {"property": "og:published_time"},
            {"name": "pubdate"},
            {"name": "publish-date"},
            {"name": "date"},
        ]

        for tag in meta_tags:
            meta = soup.find("meta", tag)
            if meta:
                published_date = meta.get("content")
                if published_date:
                    break

    # JSON-LD date
    if not published_date:
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)

                if isinstance(data, dict):
                    if "datePublished" in data:
                        published_date = data["datePublished"]
                        break

            except:
                continue

    if not published_date:
        published_date = "Unknown Date"

    # ---------- TEXT SAFETY ----------
    if not text or len(text.strip()) == 0:
        text = soup.get_text(separator=" ", strip=True)

    # ---------- LANGUAGE ----------
    language = detect_language(text)

    # ---------- KEYWORDS ----------
    keywords = extract_keywords(text)

    # ---------- CHUNKING ----------
    chunks = chunk_text(text)

    # ---------- FINAL DATA ----------
    data = {
        "source_url": url,
        "source_type": "blog",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": "global",
        "topic_tags": keywords,
        "content_chunks": chunks
    }

    return data


# ---------- DEFAULT FALLBACK ----------
def default_response(url):
    return {
        "source_url": url,
        "source_type": "blog",
        "author": "Unknown Author",
        "published_date": "Unknown Date",
        "language": "unknown",
        "region": "global",
        "topic_tags": [],
        "content_chunks": []
    }