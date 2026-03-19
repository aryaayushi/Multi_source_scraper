import requests
from bs4 import BeautifulSoup
# from utils import detect_language, extract_keywords, chunk_text, calculate_trust_score

import requests
from bs4 import BeautifulSoup
from utils.helpers import detect_language
from utils.tagging import extract_keywords
from utils.chunking import chunk_text


def scrape_pubmed(url):

    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    text = soup.get_text()

    return {
        "source_url": url,
        "source_type": "pubmed",
        "author": "Unknown",
        "published_date": "Unknown Date",
        "language": detect_language(text),
        "region": "global",
        "topic_tags": extract_keywords(text),
        "content_chunks": chunk_text(text)
    }

def scrape_pubmed(url):

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    # ---------- Title ----------
    title_tag = soup.find("h1", class_="heading-title")
    title = title_tag.text.strip() if title_tag else ""

    # ---------- Authors ----------
    authors = soup.find_all("a", class_="full-name")
    author_list = [a.text.strip() for a in authors]

    author = ", ".join(author_list) if author_list else "unknown"

    # ---------- Publication Date ----------
    citation = soup.find("span", class_="cit")
    published_date = citation.text.strip() if citation else "unknown"

    # ---------- Journal ----------
    journal_tag = soup.find("button", class_="journal-actions-trigger")
    journal = journal_tag.text.strip() if journal_tag else "unknown"

    # ---------- Abstract ----------
    abstract_tag = soup.find("div", class_="abstract-content")

    abstract_text = ""
    if abstract_tag:
        abstract_text = abstract_tag.text.strip()

    # Combine title + abstract for processing
    content = title + "\n" + abstract_text

    # ---------- Language ----------
    language = detect_language(content)

    # ---------- Topic Tags ----------
    keywords = extract_keywords(content)

    # ---------- Content Chunks ----------
    chunks = chunk_text(content)

    # ---------- Region ----------
    # PubMed articles usually do not provide region directly
    region = "global"

    data = {
        "source_url": url,
        "source_type": "pubmed",
        "author": author,
        "published_date": published_date,
        "language": language,
        "region": region,
        "topic_tags": keywords,
        
        "content_chunks": chunks
    }

    return data