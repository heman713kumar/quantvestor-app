from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

ALLOWED_ORIGINS = ["*"]  # lock down later to your Netlify domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_ticker(url: str) -> str:
    # works for https://finance.yahoo.com/quote/EMUDHRA.NS
    m = re.search(r"/quote/([A-Za-z0-9\.\-:_]+)", url)
    return m.group(1) if m else "UNKNOWN"

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/valuation")
def valuation(url: str = Query(...)):
    ticker = parse_ticker(url)
    # TODO: replace with real scraping & your models
    return {
        "ticker": ticker,
        "valuations": [
            {"model": "DCF", "target": 388.14, "entry": 258.76, "note": "10y FCF, 7.3% discount"},
            {"model": "PE (7Y Avg)", "target": 230.85, "entry": 153.75, "note": "Forward EPS × historical PE"},
            {"model": "EV/EBITDA", "target": 214.79, "entry": 143.19, "note": "EV/EBITDA multiple"},
            {"model": "Graham (old)", "target": 150.88, "note": "EPS × (8.5 + 2g)"},
        ],
        "sentiment": {"scorePct": 62, "label": "Positive"},
    }
