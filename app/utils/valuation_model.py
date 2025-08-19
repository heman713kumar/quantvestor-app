def calculate_dcf(eps, growth, discount_rate=0.1, years=5):
    if eps is None or eps <= 0:
        return 0.0, "DCF not computed: EPS missing or = 0."
    if growth is None or growth <= 0 or growth >= discount_rate:
        growth = 0.05
    eps_list = [eps * ((1 + growth) ** i) for i in range(1, years + 1)]
    discounted = [eps_list[i] / ((1 + discount_rate) ** (i + 1)) for i in range(years)]
    terminal_value = eps_list[-1] * (1 + growth) / (discount_rate - growth)
    terminal_discounted = terminal_value / ((1 + discount_rate) ** years)
    value = sum(discounted) + terminal_discounted
    return value, f"DCF using {years} yrs growth at {growth*100:.1f}%, discounted at {discount_rate*100:.1f}%."

def calculate_pe(eps, avg_pe=20):
    if eps is None or eps <= 0:
        return 0.0, "PE not computed: EPS missing or = 0."
    value = eps * avg_pe
    return value, f"PE valuation using EPS={eps:.2f}, PE={avg_pe}."

def calculate_graham(eps, growth):
    if eps is None or eps <= 0:
        return 0.0, "Graham not computed: EPS missing or = 0."
    g = (growth or 0.05) * 100
    value = eps * (8.5 + 2 * g)
    return value, f"Graham formula with EPS={eps:.2f}, growth={g:.1f}%."

def calculate_all_valuations(data):
    eps = data.get("eps_ttm") or 0
    growth = data.get("growth_estimate") or 0.05
    dcf_val, dcf_exp = calculate_dcf(eps, growth)
    pe_val, pe_exp = calculate_pe(eps)
    graham_val, graham_exp = calculate_graham(eps, growth)
    return {
        "DCF": {"value": round(dcf_val, 2), "explanation": dcf_exp},
        "PE": {"value": round(pe_val, 2), "explanation": pe_exp},
        "Graham": {"value": round(graham_val, 2), "explanation": graham_exp},
    }
