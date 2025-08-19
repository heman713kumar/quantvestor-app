from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from app.utils.yahoo_scraper import scrape_yahoo_data
from app.utils.valuation_model import calculate_all_valuations
from app.utils.sentiment_analysis import analyze_sentiment

app = FastAPI()

# CORS for frontend (open; restrict if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValuationRequest(BaseModel):
    url: str

class SentimentRequest(BaseModel):
    query: str

class BulkValuationRequest(BaseModel):
    urls: List[str]

@app.post("/valuation")
async def get_valuation(data: ValuationRequest):
    try:
        stock_data = scrape_yahoo_data(data.url)
        valuation = calculate_all_valuations(stock_data)
        return { "success": True, "data": valuation }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment")
async def get_sentiment(data: SentimentRequest):
    try:
        sentiment_data = analyze_sentiment(data.query)
        return { "success": True, "data": sentiment_data }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bulk-valuation")
async def bulk_valuation(data: BulkValuationRequest):
    try:
        results: Dict[str, Dict] = {}
        for url in data.urls:
            sd = scrape_yahoo_data(url)
            val = calculate_all_valuations(sd)
            ticker = url.rstrip("/").split("/")[-1].split("?")[0].upper()
            results[ticker] = val
        return { "success": True, "data": results }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
