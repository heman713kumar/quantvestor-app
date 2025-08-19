def _safe(v, default=0.0):
    try:
        return float(v) if v is not None else default
    except Exception:
        return default

def calculate_dcf(eps, growth, discount_rate=0.10, years=5):
    eps = _safe(eps)
    growth = _safe(growth, 0.05)
    if eps <= 0:
        return 0.0, "DCF not computed: EPS ≤ 0."
    if growth <= 0 or growth >= discount_rate:
        growth = 0.05  # guardrail

    # very lightweight EPS-based proxy DCF (not rigorous—good demo)
    eps_proj = [eps * ((1 + growth) ** i) for i in range(1, years + 1)]
    pv = sum(eps_proj[i] / ((1 + discount_rate) ** (i + 1)) for i in range(years))
    terminal = eps_proj[-1] * (1 + growth) / (discount_rate - growth)
    pv_terminal = terminal / ((1 + discount_rate) ** years)
    value = pv + pv_terminal
    return value, f"DCF: {years}y growth @ {growth*100:.1f}%, discount {discount_rate*100:.1f}%."

def calculate_pe(eps, avg_pe=20):
    eps = _safe(eps)
    if eps <= 0:
        return 0.0, "PE not computed: EPS ≤ 0."
    return eps * avg_pe, f"PE multiple: EPS={eps:.2f}, P/E={avg_pe}."

def calculate_graham(eps, growth):
    eps = _safe(eps)
    g = _safe(growth, 0.05)
    if eps <= 0:
        return 0.0, "Graham not computed: EPS ≤ 0."
    g100 = g * 100.0
    value = eps * (8.5 + 2 * g100)
    return value, f"Graham: EPS={eps:.2f}, growth={g100:.1f}%."

def calculate_all_valuations(data: dict):
    eps = data.get("eps_ttm")
    growth = data.get("growth_estimate")
    dcf_v, dcf_e = calculate_dcf(eps, growth)
    pe_v, pe_e = calculate_pe(eps)
    gr_v, gr_e = calculate_graham(eps, growth)

    return {
        "DCF":    {"value": round(dcf_v, 2), "explanation": dcf_e},
        "PE":     {"value": round(pe_v, 2),  "explanation": pe_e},
        "Graham": {"value": round(gr_v, 2),  "explanation": gr_e},
    }
