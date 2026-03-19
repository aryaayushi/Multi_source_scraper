import json
import os
from scoring.trust_score import calculate_trust_score
from scraper.blog_scraper import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper import scrape_pubmed




# ---------------- URLS ----------------
blog_urls = [
    "https://towardsai.net/p/l/research-article-meta-data-description-made-quick-and-easy-2",
    "https://home.mlops.community/public/blogs/what-reads-impacted-my-ml-engineering-journey-most",
    "https://www.healthline.com/health/diabetes",  # good (has disclaimer)
    "https://randomhealthblog.com/diabetes-cure",   # edge case (no metadata)
    "https://towardsdatascience.com/understanding-neural-networks-19020b758230",
    "https://paulgraham.com/ai.html",
    "https://httpbin.org/html"
    
]

youtube_urls = [
    "https://www.youtube.com/watch?v=aircAruvnKk",
    "https://www.youtube.com/watch?v=IHZwWFHWa-w",
    "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
    
]

pubmed_urls = [
    "https://pubmed.ncbi.nlm.nih.gov/31452104/",
    "https://pubmed.ncbi.nlm.nih.gov/11005747/"
]


# ---------------- CREATE OUTPUT FOLDER ----------------
os.makedirs("scraped_data", exist_ok=True)


# ---------------- BLOG SCRAPING ----------------
blogs = []

for url in blog_urls:
    try:
        data = scrape_blog(url)

        # Combine content
        text = " ".join(data.get("content_chunks", []))

        # Add trust score
        data["trust_score"] = calculate_trust_score(
            url,
            data.get("author"),
            text,
            data.get("published_date")
        )

        blogs.append(data)

    except Exception as e:
        print(f"[BLOG ERROR] {url}")
        print(e)


# ---------------- YOUTUBE SCRAPING ----------------
youtube_data = []

for url in youtube_urls:
    try:
        data = scrape_youtube(url)

        text = " ".join(data.get("content_chunks", []))

        data["trust_score"] = calculate_trust_score(
            url,
            data.get("author"),
            text,
            data.get("published_date")
        )

        youtube_data.append(data)

    except Exception as e:
        print(f"[YOUTUBE ERROR] {url}")
        print(e)


# ---------------- PUBMED SCRAPING ----------------
pubmed_data = []

for url in pubmed_urls:
    try:
        data = scrape_pubmed(url)

        text = " ".join(data.get("content_chunks", []))

        data["trust_score"] = calculate_trust_score(
            url,
            data.get("author"),
            text,
            data.get("published_date")
        )

        pubmed_data.append(data)

    except Exception as e:
        print(f"[PUBMED ERROR] {url}")
        print(e)


# ---------------- SAVE OUTPUT ----------------
with open("scraped_data/blogs.json", "w", encoding="utf-8") as f:
    json.dump(blogs, f, indent=4, ensure_ascii=False)

with open("scraped_data/youtube.json", "w", encoding="utf-8") as f:
    json.dump(youtube_data, f, indent=4, ensure_ascii=False)

with open("scraped_data/pubmed.json", "w", encoding="utf-8") as f:
    json.dump(pubmed_data, f, indent=4, ensure_ascii=False)


# ---------------- COMBINED FILE (IMPORTANT FOR SUBMISSION) ----------------
all_data = blogs + youtube_data + pubmed_data

with open("scraped_data/all_sources.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)


print("✅ Scraping Completed Successfully!")
print(f"Blogs: {len(blogs)}, YouTube: {len(youtube_data)}, PubMed: {len(pubmed_data)}")