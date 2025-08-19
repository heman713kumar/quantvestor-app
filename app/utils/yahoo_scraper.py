import yfinance as yf

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
