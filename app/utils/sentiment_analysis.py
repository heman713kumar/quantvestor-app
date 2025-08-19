from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

def analyze_sentiment(query: str) -> dict:
    try:
        url = f"https://news.google.com/search?q={query}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        headlines = [h.text for h in soup.select("article h3")][:5]
        scores = [TextBlob(h).sentiment.polarity for h in headlines]
        avg = round(sum(scores)/len(scores), 3) if scores else 0.0
        return {
            "score": avg,
            "headlines": headlines,
            "explanation": "Average TextBlob polarity of latest Google News headlines."
        }
    except Exception as e:
        raise ValueError(f"Sentiment analysis failed: {e}")
