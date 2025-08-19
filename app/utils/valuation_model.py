# utils/valuation_model.py

def calculate_intrinsic_value(ticker: str) -> list:
    """
    Placeholder valuation models — replace with real logic or Excel logic replication.
    """
    return [
        {"model": "DCF", "target": 388.14, "entry": 258.76, "note": "10y FCF, 7.3% discount"},
        {"model": "PE (7Y Avg)", "target": 230.85, "entry": 153.75, "note": "Forward EPS × historical PE"},
        {"model": "EV/EBITDA", "target": 214.79, "entry": 143.19, "note": "EV/EBITDA multiple"},
        {"model": "Graham (old)", "target": 150.88, "note": "EPS × (8.5 + 2g)"},
    ]
