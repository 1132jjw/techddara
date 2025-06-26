# fetch_news.py (OpenAI SDK v1.x 호환 버전)
import feedparser
import requests
from bs4 import BeautifulSoup
import openai
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. ArXiv에서 최신 논문 가져오기 (기본 summary 제공)
def fetch_arxiv_rss(limit=5, category="cs.AI"):
    url = f"http://export.arxiv.org/rss/{category}"
    feed = feedparser.parse(url)
    return [
        {
            "source": "arxiv",
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link
        }
        for entry in feed.entries[:limit]
    ]

# 2. Hacker News 인기 뉴스 수집
def fetch_hackernews_rss(limit=5):
    url = "https://hnrss.org/frontpage"
    feed = feedparser.parse(url)
    return [
        {
            "source": "hackernews",
            "title": entry.title,
            "link": entry.link
        }
        for entry in feed.entries[:limit]
    ]

# 3. Hacker News 뉴스의 외부 기사 일부 본문 추출 (요약용)
def get_article_text(url, max_paragraphs=5):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.text for p in paragraphs[:max_paragraphs])
    except Exception:
        return None
