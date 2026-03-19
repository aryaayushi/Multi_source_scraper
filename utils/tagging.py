from collections import Counter
import re

def extract_keywords(text, top_n=5):

    words = re.findall(r'\w+', text.lower())

    stopwords = set([
        "the", "is", "in", "and", "to", "of", "a", "for", "on", "with"
    ])

    filtered = [w for w in words if w not in stopwords and len(w) > 3]

    most_common = Counter(filtered).most_common(top_n)

    return [word for word, _ in most_common]