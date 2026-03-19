# Multi-Source Web Scraper & Trust Score System

## 📌 Project Overview

This project is a **multi-source web scraping system** that extracts structured data from different types of online sources and evaluates their reliability using a custom **Trust Scoring Algorithm**.

The system supports:

* 📰 Blog articles
* 🎥 YouTube videos
* 🧬 PubMed research papers

Each source is scraped, processed, and stored in a structured JSON format, along with a computed trust score.

---

## 🛠️ Tools and Libraries Used

### 🔹 Core Libraries

* `requests` – For fetching web pages
* `BeautifulSoup (bs4)` – For HTML parsing
* `newspaper3k` – For extracting blog content
* `yt-dlp` – For extracting YouTube metadata
* `youtube-transcript-api` – For video transcripts
* `langdetect` – For language detection
* `yake` – For keyword extraction
* `json` – For structured data storage

---

## ⚙️ Scraping Approach

### 1️⃣ Blog Scraping

* Extracts:

  * Author (from newspaper / meta / JSON-LD)
  * Publish date (meta tags / schema)
  * Full article text
* Removes unwanted elements like ads and navigation
* Uses fallback strategies when metadata is missing

---

### 2️⃣ YouTube Scraping

* Extracts:

  * Channel name (author)
  * Upload date
  * Description
  * Transcript (if available)
* If transcript is unavailable → uses description as fallback

---

### 3️⃣ PubMed Scraping

* Extracts:

  * Article title
  * Authors
  * Abstract
  * Journal
  * Publication year
* Handles multiple authors and structured scientific metadata

---

### 4️⃣ Content Processing

* **Language Detection** → using `langdetect`
* **Keyword Extraction** → using `yake`
* **Content Chunking** → splits long text into smaller segments

---

## 📊 Trust Score Design

The trust score is calculated in the range **0 to 1** using the formula:

```
Trust Score = f(
    domain_authority,
    author_credibility,
    content_quality,
    recency
)
```

### 🔹 Factors Considered

#### ✅ Domain Authority

* High trust: `.gov`, `.edu`, PubMed
* Medium: Medium, TowardsAI
* Low: Unknown/random domains

---

#### ✅ Author Credibility

* Known author → higher score
* Missing/unknown → penalty

---

#### ✅ Content Quality

* Based on article length:

  * Long content → high score
  * Short content → low score

---

#### ✅ Recency

* Recent content → higher score
* Old content → penalty applied

---

## ⚠️ Edge Cases Handled

* Missing metadata (author/date)
* No YouTube transcript
* Multiple authors (averaged credibility)
* Non-English content
* Long articles (chunking works properly)

---

## 🔐 Abuse Prevention Logic

### 🚫 Fake Authors

* Unknown authors are penalized

### 🚫 SEO Spam Blogs

* Low-authority domains receive lower scores

### 🚫 Misleading Medical Content

* Lack of disclaimer reduces trust score

### 🚫 Outdated Information

* Older content receives recency penalty

---

## 📁 Project Structure

```
Multi_source_web_scrapper/
│
├── scraper/
│   ├── blog_scraper.py
│   ├── youtube_scraper.py
│   ├── pubmed_scraper.py
│
├── scoring/
│   └── trust_score.py
│
├── utils/
│   ├── helpers.py
│   ├── tagging.py
│   ├── chunking.py
│
├── scraped_data/
│   ├── blogs.json
│   ├── youtube.json
│   ├── pubmed.json
│   └── all_sources.json
│
├── main.py
└── README.md
```

---

## ▶️ How to Run the Project

### Step 1: Install Dependencies

```bash
pip install requests beautifulsoup4 newspaper3k yt-dlp youtube-transcript-api langdetect yake
```

---

### Step 2: Navigate to Project Folder

```bash
cd Multi_source_web_scrapper
```

---

### Step 3: Run the Script

```bash
python main.py
```

---

### Step 4: Check Output

Results will be stored in:

```
scraped_data/
```

Files generated:

* `blogs.json`
* `youtube.json`
* `pubmed.json`
* `all_sources.json`

---

## ⚠️ Limitations

* Some websites block scraping (SSL / bot protection)
* YouTube transcripts may not always be available
* Author/date may be missing for poorly structured blogs
* Domain authority is rule-based (not using real SEO APIs)
* Trust score is heuristic, not fully AI-based

---

## 🚀 Future Improvements

* Integrate real domain authority APIs
* Improve author credibility using external sources (LinkedIn / Google Scholar)
* Add machine learning-based trust scoring
* Build a web UI dashboard for visualization

---

## 👩‍💻 Author

Ayushi Arya

---

## ⭐ Conclusion

This project demonstrates a complete pipeline for:

* Multi-source data extraction
* Text processing
* Reliability scoring

It is designed to be **robust, modular, and scalable**, handling real-world edge cases effectively.
