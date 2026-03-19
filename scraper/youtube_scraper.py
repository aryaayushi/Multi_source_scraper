import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

from utils.helpers import detect_language
from utils.tagging import extract_keywords
from utils.chunking import chunk_text


def get_video_id(url):
    try:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be" in url:
            return url.split("/")[-1]
    except:
        pass
    return None


def scrape_youtube(url):

    # ---------- DEFAULT FALLBACK ----------
    data = {
        "source_url": url,
        "source_type": "youtube",
        "author": "Unknown",
        "published_date": "Unknown Date",
        "language": "unknown",
        "region": "global",
        "topic_tags": [],
        "content_chunks": []
    }

    try:
        # ---------- METADATA ----------
        ydl_opts = {
            "quiet": True,
            "skip_download": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # ---------- AUTHOR ----------
        author = info.get("channel") or info.get("uploader") or "Unknown"

        # ---------- DATE ----------
        published_date = info.get("upload_date")

        if published_date:
            published_date = f"{published_date[:4]}-{published_date[4:6]}-{published_date[6:]}"
        else:
            published_date = "Unknown Date"

        # ---------- DESCRIPTION ----------
        description = info.get("description", "")

        # ---------- REGION ----------
        region = info.get("uploader_country") or "global"

        # ---------- TRANSCRIPT ----------
        video_id = get_video_id(url)

        transcript_text = ""
        chunks = []

        if video_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)

                for line in transcript:
                    text = line.get("text", "")
                    transcript_text += text + " "
                    chunks.append(text)

            except:
                # fallback to description
                transcript_text = description
                chunks = chunk_text(description)

        else:
            transcript_text = description
            chunks = chunk_text(description)

        # ---------- LANGUAGE ----------
        language = detect_language(transcript_text)

        # ---------- KEYWORDS ----------
        keywords = extract_keywords(transcript_text)

        # ---------- FINAL DATA ----------
        data.update({
            "author": author,
            "published_date": published_date,
            "language": language,
            "region": region,
            "topic_tags": keywords,
            "content_chunks": chunks
        })

    except Exception as e:
        print(f"[YOUTUBE ERROR] {url}")
        print(e)

    return data