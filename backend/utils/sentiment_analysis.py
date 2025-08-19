# utils/sentiment_analysis.py

from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a given string using TextBlob.
    Returns a sentiment score (%) and label.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1

    score_pct = int((polarity + 1) * 50)  # Normalize to 0–100
    label = (
        "Positive" if polarity > 0.2 else
        "Negative" if polarity < -0.2 else
        "Neutral"
    )

    return {"scorePct": score_pct, "label": label}
