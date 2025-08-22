# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

# Your utils (already in your repo)
from app.utils.yahoo_scraper import scrape_yahoo_data
from app.utils.valuation_model import calculate_valuations
from app.utils.sentiment_analysis import analyze_sentiment

app = FastAPI(title="QuantVestor API", version="1.0.0")

# --- CORS so the Vite dev server can call us locally ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

# --------- Schemas ---------
class ValuationRequest(BaseModel):
    # accept either a Yahoo URL OR a plain ticker
    url: Optional[str] = None
    ticker: Optional[str] = None

class BulkValuationRequest(BaseModel):
    urls: List[HttpUrl]

class SentimentRequest(BaseModel):
    query: str  # ticker, company name, etc.


# --------- Helpers ---------
def _as_yahoo_url(ticker_or_url: str) -> str:
    """Return a Yahoo Finance quote URL from either a ticker or a URL."""
    s = (ticker_or_url or "").strip()
    if not s:
        raise ValueError("Empty ticker/URL")
    if s.lower().startswith("http"):
        return s
    ticker = s.split("?")[0].upper()
    return f"https://finance.yahoo.com/quote/{ticker}"

def _run_valuation(yahoo_url: str) -> Dict[str, Any]:
    """
    1) Scrape/collect inputs
    2) Run your valuation model(s)
    Must return { DCF: {value, explanation}, PE: {...}, Graham: {...} }
    """
    data = scrape_yahoo_data(yahoo_url)          # expected to return a dict your model understands
    valuations = calculate_valuations(data)      # expected shape as above
    return valuations


# --------- Routes ---------
@app.get("/")
def root():
    return {"ok": True, "service": "quantvestor-backend", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/valuation")
def valuation(req: ValuationRequest):
    try:
        base = req.url or req.ticker
        if not base:
            raise HTTPException(status_code=400, detail="Provide either 'url' or 'ticker'")
        url = _as_yahoo_url(base)
        result = _run_valuation(url)
        return {"success": True, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"valuation failed: {e}")

@app.post("/bulk-valuation")
def bulk_valuation(req: BulkValuationRequest):
    try:
        out: Dict[str, Any] = {}
        for url in req.urls:
            try:
                result = _run_valuation(str(url))
                # key by ticker symbol (last path segment) for easy lookup on the frontend
                key = str(url).rstrip("/").split("/")[-1].split("?")[0].upper()
                out[key] = result
            except Exception as e:
                out[str(url)] = {"error": str(e)}
        return {"success": True, "data": out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"bulk valuation failed: {e}")

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    try:
        res = analyze_sentiment(req.query)
        # expected to be: {score: -1..1, headlines: [...], explanation: "..."}
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"sentiment failed: {e}")
