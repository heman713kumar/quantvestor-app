from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from app.utils.yahoo_scraper import scrape_yahoo_data
from app.utils.valuation_model import calculate_all_valuations
from app.utils.sentiment_analysis import analyze_sentiment

app = FastAPI(title="QuantVestor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod
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

@app.get("/")
def root():
    return {"ok": True, "service": "quantvestor-backend"}

@app.post("/valuation")
def valuation(data: ValuationRequest):
    try:
        stock = scrape_yahoo_data(data.url)
        vals = calculate_all_valuations(stock)
        return {"success": True, "data": vals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bulk-valuation")
def bulk_valuation(data: BulkValuationRequest):
    try:
        result: Dict[str, Dict] = {}
        for u in data.urls:
            stock = scrape_yahoo_data(u)
            vals = calculate_all_valuations(stock)
            key = stock["ticker"].upper()
            result[key] = vals
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment")
def sentiment(data: SentimentRequest):
    try:
        res = analyze_sentiment(data.query)
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
