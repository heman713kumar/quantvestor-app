import yfinance as yf

def scrape_yahoo_data(url: str):
    try:
        ticker_symbol = url.strip('/').split('/')[-1].split('?')[0]
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        return {
            "ticker": ticker_symbol,
            "current_price": info.get("currentPrice"),
            "eps_ttm": info.get("trailingEps"),
            "growth_estimate": info.get("earningsQuarterlyGrowth"),
            "book_value": info.get("bookValue"),
            "pe_ratio": info.get("trailingPE"),
            "roe": info.get("returnOnEquity"),
        }
    except Exception as e:
        raise ValueError(f"Failed to fetch data: {str(e)}")
