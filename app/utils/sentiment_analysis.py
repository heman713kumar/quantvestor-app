from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

def analyze_sentiment(query: str) -> dict:
    try:
        search_url = f"https://news.google.com/search?q={query}"
        r = requests.get(search_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        headlines = [tag.text for tag in soup.select("article h3")][:5]
        sentiments = [(TextBlob(h).sentiment.polarity) for h in headlines]
        avg_score = sum(sentiments) / len(sentiments) if sentiments else 0.0
        return {
            "score": round(avg_score, 3),
            "headlines": headlines,
            "explanation": "Average TextBlob polarity of latest Google News headlines."
        }
    except Exception as e:
        raise ValueError(f"Sentiment analysis failed: {str(e)}")
