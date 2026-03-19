from urllib.parse import urlparse
from datetime import datetime


def calculate_trust_score(url, author, text, published_date):
    score = 0.0

    # ---------- DOMAIN AUTHORITY ----------
    domain = urlparse(url).netloc

    if any(x in domain for x in ["gov", "edu", "nih", "who.int"]):
        domain_score = 1.0
    elif any(x in domain for x in ["medium", "towardsai", "mlops"]):
        domain_score = 0.6
    else:
        domain_score = 0.4

    # ---------- AUTHOR CREDIBILITY ----------
    if author and author not in ["Unknown Author", "unknown"]:
        author_score = 0.8
    else:
        author_score = 0.3

    # ---------- CONTENT QUALITY ----------
    word_count = len(text.split())

    if word_count > 1500:
        content_score = 1.0
    elif word_count > 500:
        content_score = 0.7
    else:
        content_score = 0.4

        # //add medical logic
    if "medical" in text.lower():
        if "disclaimer" in text.lower():
            medical_score = 1.0
        else:
            medical_score = 0.3

    # ---------- RECENCY ----------
    recency_score = 0.5  # default

    if published_date and published_date != "Unknown Date":
        try:
            pub_date = datetime.fromisoformat(published_date[:10])
            days_old = (datetime.now() - pub_date).days

            if days_old < 365:
                recency_score = 1.0
            elif days_old < 3 * 365:
                recency_score = 0.7
            else:
                recency_score = 0.3
        except:
            pass

    # ---------- FINAL SCORE ----------
    score = (
        0.3 * domain_score +
        0.2 * author_score +
        0.3 * content_score +
        0.2 * recency_score
    )

    return round(score, 2)