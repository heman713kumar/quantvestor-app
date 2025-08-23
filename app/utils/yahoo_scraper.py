import yfinance as yf

# keep your existing scrape_yahoo_data(...)
def parse_ticker(input_or_url: str) -> str:
    s = (input_or_url or "").strip()
    if not s:
        return ""
    if s.lower().startswith("http"):
        frag = s.rstrip("/").split("/")[-1].split("?")[0]
        return frag.upper()
    return s.split("?")[0].upper()

def fetch_basics(ticker: str):
    # normalize and reuse your existing function
    t = parse_ticker(ticker)
    data = scrape_yahoo_data(t)  # use your current function
    # map to the keys valuation_model expects
    return {
        "ticker": t,
        "price": data.get("current_price"),
        "eps_ttm": data.get("eps_ttm"),
        "growth": data.get("growth_estimate") if isinstance(data.get("growth_estimate"), (int, float)) else 0.05,
        "book_value": data.get("book_value"),
    }

def scrape_yahoo_data(url_or_ticker: str):
    """
    Accepts a full Yahoo URL (e.g. https://finance.yahoo.com/quote/AAPL)
    OR a bare ticker (e.g. AAPL).
    """
    t = url_or_ticker.strip()
    if t.startswith("http"):
        t = t.strip("/").split("/")[-1].split("?")[0]

    ticker = yf.Ticker(t)
    info = ticker.info or {}

    return {
        "ticker": t,
        "current_price": info.get("currentPrice"),
        "eps_ttm": info.get("trailingEps"),
        "growth_estimate": info.get("earningsQuarterlyGrowth"),  # fallback handled in valuation
        "book_value": info.get("bookValue"),
        "pe_ratio": info.get("trailingPE"),
        "roe": info.get("returnOnEquity"),
    }
