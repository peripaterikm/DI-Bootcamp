# make_metrics.py — compute derived macro metrics for the Israel dashboard
# I read the wide dataset produced by make_dataset.py and create a "core enhanced" file,
# generate charts, write a summary, and inject a chart gallery into REPORT.md.

from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

# ====== PATHS (my local layout) ======
BASE  = Path(r"C:\DI-Bootcamp\FinalProject\AllTogether")
OUT   = BASE / "Out"
PLOTS = OUT / "plots"
OUT.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)

WIDE_CSV   = OUT / "israel_economy_wide.csv"
CORE_OUT   = OUT / "israel_economy_core_enhanced.csv"
SUMMARY_MD = OUT / "CORE_SUMMARY.md"
REPORT_MD  = OUT / "REPORT.md"

# ====== FOCUS WINDOW (for clearer charts) ======
YEARS_FOCUS = 15  # change to 10 if I want a shorter window

def last_n_years(s: pd.Series, years: int = YEARS_FOCUS) -> pd.Series:
    """Keep only the last N years (based on the series index)."""
    if s is None or s.dropna().empty:
        return s
    end = s.index.max()
    start = end - pd.DateOffset(years=years)
    return s.loc[s.index >= start]

# ====== helpers ======
def safe_write_csv(df: pd.DataFrame, path: Path):
    """I want the write to succeed even if the file is open elsewhere."""
    try:
        df.to_csv(path)
        print("  Saved:", path)
    except PermissionError:
        ts = time.strftime("%Y%m%d_%H%M%S")
        alt = path.with_name(path.stem + f"_{ts}.csv")
        df.to_csv(alt)
        print(f"  [WARN] {path} is in use; wrote to {alt} instead.")

def find_col(df: pd.DataFrame, exact: str, fallbacks: list[str] | None = None) -> str | None:
    """
    I try to locate a column by its expected series_id. If it's missing,
    I fall back to a simple substring search over column names.
    """
    cols = list(df.columns)
    if exact in cols:
        return exact
    if fallbacks:
        for fb in fallbacks:
            if fb in cols:
                return fb
    key = exact.lower().replace("__", "_")
    for c in cols:
        cl = c.lower()
        if all(k in cl for k in key.split("_")):
            return c
    return None

# --- robust percent changes ---
def yoy_pct_safe(s: pd.Series) -> pd.Series:
    """12-month percent change in %, robust to zero/negative base and wild outliers."""
    x = pd.to_numeric(s, errors="coerce")
    prev = x.shift(12)
    bad_base = prev.abs() <= 1e-9
    out = (x / prev - 1.0) * 100.0
    out[bad_base] = np.nan
    out[np.abs(out) > 150] = np.nan
    return out

def mom_pct(s: pd.Series) -> pd.Series:
    """1-month percent change in % (basic)."""
    x = pd.to_numeric(s, errors="coerce")
    out = x.pct_change(1) * 100.0
    out[np.abs(out) > 150] = np.nan
    return out

def index_to_100(s: pd.Series) -> pd.Series:
    """Index a series to 100 at the first valid observation."""
    s = pd.to_numeric(s, errors="coerce")
    first_valid = s.dropna()
    if first_valid.empty:
        return s * np.nan
    base = first_valid.iloc[0]
    if not pd.notna(base) or base == 0:
        return s * np.nan
    return (s / base) * 100.0

def zscore(s: pd.Series) -> pd.Series:
    """Standardize to mean 0 / std 1, safe for NaNs and constants."""
    s = pd.to_numeric(s, errors="coerce")
    mu, sd = s.mean(skipna=True), s.std(skipna=True)
    if pd.isna(sd) or sd == 0:
        return s * np.nan
    return (s - mu) / sd

def plot_series(ts: pd.Series, title: str, filename: str, ylabel: str = "") -> Path:
    """Make a simple, clean matplotlib line chart (no custom styles/colors)."""
    plt.figure()
    ts.dropna().plot()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.tight_layout()
    out = PLOTS / filename
    plt.savefig(out, dpi=160)
    plt.close()
    return out

# ---- CPI chain-linked YoY (rebasing-proof) ----
def cpi_chain_yoy_from_level(level: pd.Series) -> pd.Series:
    """
    Compute CPI YoY via chain-linking monthly ratios. I treat absurd MoM spikes
    (|MoM| > 5% since 2000-01-01) as technical rebases and set their monthly ratio to 1.0.
    """
    x = pd.to_numeric(level, errors="coerce")
    r = x / x.shift(1)  # monthly ratio
    mom_pct_raw = (r - 1.0) * 100.0

    modern = r.index >= "2000-01-01"
    bad = modern & (mom_pct_raw.abs() > 5.0)
    r[bad] = 1.0  # ignore rebase jump

    # 12-month chain product minus 1
    yoy = (r.rolling(12).apply(lambda a: np.prod(a), raw=True) - 1.0) * 100.0
    return yoy

def clean_index_level(s: pd.Series) -> pd.Series:
    """CPI/HPI levels should be strictly >0; replace zeros/negatives with NaN."""
    x = pd.to_numeric(s, errors="coerce")
    return x.where(x > 0)

def derive_cpi_yoy(cpi_level: pd.Series | None, cpi_yoy_candidate: pd.Series | None) -> pd.Series | None:
    """
    Prefer a reasonable-looking YoY if present; otherwise compute robust chain-linked YoY.
    """
    def looks_like_yoy_percent(s: pd.Series) -> bool:
        v = pd.to_numeric(s, errors="coerce").dropna()
        if v.empty:
            return False
        share_in_band = (v.between(-20, 50)).mean()
        med_abs = v.abs().median()
        return (share_in_band >= 0.9) and (med_abs <= 10)

    if cpi_yoy_candidate is not None and looks_like_yoy_percent(cpi_yoy_candidate):
        y = pd.to_numeric(cpi_yoy_candidate, errors="coerce")
        y[np.abs(y) > 150] = np.nan
        return y

    if cpi_level is not None:
        lvl = clean_index_level(cpi_level)
        return cpi_chain_yoy_from_level(lvl)

    return None

# ====== load ======
wide = pd.read_csv(WIDE_CSV, parse_dates=["date"]).set_index("date").sort_index()

# ====== map required series (robust to minor id drift) ======
sid = {}
sid["cpi_index"]   = find_col(wide, "cpi_total_index")
sid["cpi_yoy_col"] = find_col(wide, "cpi_yoy", fallbacks=["cpi_total_yoy","cpi_yoy_pct","inflation_yoy"])  # optional
sid["rate"]        = find_col(wide, "boi_policy_rate_pct")
sid["unemp"]       = find_col(wide, "unemployment_25_64_pct", fallbacks=["unemployment_rate_25_64_pct"])
sid["wage_real"]   = find_col(wide, "real_wage_avg_monthly")
sid["hpi"]         = find_col(wide, "house_price_index")
sid["mortgage"]    = find_col(wide, "mortgage_volume_total", fallbacks=["mortgage_volume_col1","mortgage_volumes_total"])
sid["gdp_growth"]  = find_col(wide, "gdp_growth_annual_terms_pct")
sid["usdils"]      = find_col(wide, "usd_ils")
sid["eurils"]      = find_col(wide, "eur_ils")

# ====== core frame ======
core = pd.DataFrame(index=wide.index).sort_index()

# attach raw series if present
for k in sid:
    col = sid[k]
    if col and col in wide.columns:
        core[k] = pd.to_numeric(wide[col], errors="coerce")

# ====== derived metrics ======
# CPI YoY (robust)
cpi_level = core.get("cpi_index")
cpi_yoy_candidate = core.get("cpi_yoy_col")
cpi_yoy_raw = derive_cpi_yoy(cpi_level, cpi_yoy_candidate)
if cpi_yoy_raw is not None:
    core["cpi_yoy"] = cpi_yoy_raw

# Modern-period cleaning for CPI YoY (remove technical spikes)
if "cpi_yoy" in core:
    core["cpi_yoy_clean"] = core["cpi_yoy"].copy()
    modern = core.index >= "2000-01-01"
    spike  = core["cpi_yoy_clean"].abs() > 20.0  # >20% YoY is unrealistic post-2000
    core.loc[modern & spike, "cpi_yoy_clean"] = np.nan

# Real policy rate: nominal minus *cleaned* CPI YoY
if ("rate" in core.columns) and ("cpi_yoy_clean" in core.columns):
    aligned = pd.concat([core["rate"], core["cpi_yoy_clean"]], axis=1).dropna()
    rr = aligned.iloc[:, 0] - aligned.iloc[:, 1]
    core["real_rate"] = rr.reindex(core.index)

# Rate gap vs 2% inflation target, and 12m change in rate
if "rate" in core:
    core["rate_gap"] = core["rate"] - 2.0
    core["rate_change_12m"] = core["rate"] - core["rate"].shift(12)

# Real wages: index + YoY
if "wage_real" in core:
    core["real_wage_indexed"] = index_to_100(core["wage_real"])
    core["wage_growth_12m"] = yoy_pct_safe(core["wage_real"])

# HPI: index + YoY
if "hpi" in core:
    core["hpi_total"] = core["hpi"]
    core["hpi_total_indexed"] = index_to_100(core["hpi"])
    core["hpi_growth_12m"] = yoy_pct_safe(core["hpi"])

# Affordability: (real_wage_indexed / hpi_total_indexed) * 100
if "real_wage_indexed" in core and "hpi_total_indexed" in core:
    core["affordability"] = (core["real_wage_indexed"] / core["hpi_total_indexed"]) * 100.0

# FX metrics: YoY and 12m volatility of MoM (for USD/ILS)
if "usdils" in core:
    core["fx_change_12m"] = yoy_pct_safe(core["usdils"])
    core["fx_mom_pct"] = mom_pct(core["usdils"])
    core["fx_volatility_12m"] = core["fx_mom_pct"].rolling(12).std()

# CPI MoM volatility (from level) + CPI gap from *clean* YoY
if "cpi_index" in core:
    # recompute MoM from level for volatility; cap absurd monthlies in modern period
    lvl = clean_index_level(core["cpi_index"])
    mom = (lvl / lvl.shift(1) - 1.0) * 100.0
    modern = mom.index >= "2000-01-01"
    mom.loc[modern & (mom.abs() > 5.0)] = np.nan
    core["cpi_mom_pct"] = mom
    core["inflation_volatility_12m"] = core["cpi_mom_pct"].rolling(12).std()

if "cpi_yoy_clean" in core:
    core["cpi_gap"] = core["cpi_yoy_clean"] - 2.0

# Mortgages: YoY
if "mortgage" in core:
    core["housing_loans_yoy"] = yoy_pct_safe(core["mortgage"])

# Composite indices via simple z-score averages
components_stress = []
if "cpi_gap" in core:           components_stress.append(zscore(core["cpi_gap"]))
if "fx_volatility_12m" in core: components_stress.append(zscore(core["fx_volatility_12m"]))
if "unemp" in core:             components_stress.append(zscore(core["unemp"]))
if "rate_change_12m" in core:   components_stress.append(zscore(core["rate_change_12m"]))
if "gdp_growth" in core:        components_stress.append(zscore(-core["gdp_growth"]))  # weaker growth -> more stress
if components_stress:
    core["economic_stress_index"] = pd.concat(components_stress, axis=1).mean(axis=1, skipna=True)

components_housing = []
if "hpi_growth_12m" in core:    components_housing.append(zscore(core["hpi_growth_12m"]))
if "housing_loans_yoy" in core: components_housing.append(zscore(core["housing_loans_yoy"]))
if "affordability" in core:     components_housing.append(zscore(-core["affordability"]))
if components_housing:
    core["housing_pressure_index"] = pd.concat(components_housing, axis=1).mean(axis=1, skipna=True)

# ====== save core ======
safe_write_csv(core, CORE_OUT)

# ====== charts ======
charts = []
# CPI YoY — focus on last N years (use the cleaned chain-linked series)
if "cpi_yoy_clean" in core:
    charts.append(
        plot_series(last_n_years(core["cpi_yoy_clean"]),
                    "CPI YoY (%) — last 15y",
                    "01_cpi_yoy.png", "%")
    )
if "rate" in core:
    charts.append(plot_series(core["rate"], "BOI Policy Rate (%)", "02_boi_rate.png", "%"))
if "usdils" in core:
    charts.append(plot_series(core["usdils"], "USD/ILS", "03_usdils.png", ""))
if "unemp" in core:
    charts.append(plot_series(core["unemp"], "Unemployment 25–64 (%)", "04_unemployment.png", "%"))
if "real_wage_indexed" in core:
    charts.append(plot_series(core["real_wage_indexed"], "Real Wage (indexed=100)", "05_real_wage_idx.png", "Index"))
if "hpi_growth_12m" in core:
    charts.append(plot_series(core["hpi_growth_12m"], "House Price Index YoY (%)", "06_hpi_yoy.png", "%"))
if "housing_loans_yoy" in core:
    charts.append(plot_series(core["housing_loans_yoy"], "Mortgage Volumes YoY (%)", "07_mortgage_yoy.png", "%"))
if "gdp_growth" in core:
    charts.append(plot_series(core["gdp_growth"], "GDP Growth (annual terms, %)", "08_gdp_growth.png", "%"))
# Real Policy Rate — focus on last N years (driven by cleaned CPI YoY)
if "real_rate" in core:
    charts.append(
        plot_series(last_n_years(core["real_rate"]),
                    "Real Policy Rate (%, Rate − CPI YoY) — last 15y",
                    "09_real_rate.png", "%")
    )
if "affordability" in core:
    charts.append(plot_series(core["affordability"], "Housing Affordability (index)", "10_affordability.png", "Index"))
if "economic_stress_index" in core:
    charts.append(plot_series(core["economic_stress_index"], "Economic Stress Index (z-score)", "11_macro_stress.png", "z"))
if "housing_pressure_index" in core:
    charts.append(plot_series(core["housing_pressure_index"], "Housing Pressure Index (z-score)", "12_housing_pressure.png", "z"))

# ====== summary (latest readings) ======
lines = []
lines.append(f"# Core Metrics — Latest Readings (generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})\n")
def add_line(label, col, fmt="{:.2f}"):
    if col in core.columns:
        s = core[col].dropna()
        if not s.empty:
            last_date = s.index.max()
            val = s.loc[last_date]
            try:
                vtxt = fmt.format(float(val))
            except Exception:
                vtxt = str(val)
            lines.append(f"- **{label}** — {vtxt} (as of {last_date.date()})")

add_line("CPI YoY (%)", "cpi_yoy_clean")
add_line("BOI Policy Rate (%)", "rate")
add_line("Unemployment 25–64 (%)", "unemp")
add_line("USD/ILS", "usdils")
add_line("Real Wage YoY (%)", "wage_growth_12m")
add_line("House Price YoY (%)", "hpi_growth_12m")
add_line("Mortgage Volumes YoY (%)", "housing_loans_yoy")
add_line("GDP Growth (annual terms, %)", "gdp_growth")
add_line("Real Policy Rate (%, Rate − CPI YoY)", "real_rate")
add_line("Affordability (wage/HPI, index)", "affordability", "{:.1f}")
add_line("Economic Stress Index (z-score)", "economic_stress_index", "{:.2f}")
add_line("Housing Pressure Index (z-score)", "housing_pressure_index", "{:.2f}")

SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")
print("  Saved:", SUMMARY_MD)

# --- Inject a "Key Charts" gallery into REPORT.md (auto) ---
order = [
    ("01_cpi_yoy.png",            "CPI YoY (%) — last 15y"),
    ("02_boi_rate.png",           "BOI Policy Rate (%)"),
    ("09_real_rate.png",          "Real Policy Rate (%, Rate − CPI YoY) — last 15y"),
    ("06_hpi_yoy.png",            "House Price Index YoY (%)"),
    ("10_affordability.png",      "Housing Affordability (index)"),
    ("07_mortgage_yoy.png",       "Mortgage Volumes YoY (%)"),
    ("04_unemployment.png",       "Unemployment 25–64 (%)"),
    ("03_usdils.png",             "USD/ILS"),
    ("08_gdp_growth.png",         "GDP Growth (annual terms, %)"),
    ("11_macro_stress.png",       "Economic Stress Index (z)"),
    ("12_housing_pressure.png",   "Housing Pressure Index (z)"),
]
items = [(fn, title) for fn, title in order if (PLOTS / fn).exists()]
if items:
    rows = []
    for i in range(0, len(items), 2):
        cells = []
        for j in range(2):
            if i + j < len(items):
                fn, title = items[i + j]
                cells.append(
                    f'<td style="vertical-align:top; text-align:center; padding:8px;">'
                    f'<div><b>{title}</b></div>'
                    f'<img src="plots/{fn}" width="420" alt="{title}"/>'
                    f'</td>'
                )
            else:
                cells.append("<td></td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    gallery_html = "\n".join(rows)
    section = "\n".join([
        "## Key Charts",
        "",
        "<table>",
        gallery_html,
        "</table>",
        ""
    ])
    start_marker = "<!-- KEY_CHARTS_START -->"
    end_marker   = "<!-- KEY_CHARTS_END -->"
    try:
        txt = REPORT_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        txt = "# Israel Economy — Final Project Report\n"
    if start_marker in txt and end_marker in txt:
        pre = txt.split(start_marker)[0]
        post = txt.split(end_marker)[-1]
        new_txt = pre + start_marker + "\n" + section + "\n" + end_marker + post
    else:
        new_txt = txt.rstrip() + "\n\n" + start_marker + "\n" + section + "\n" + end_marker + "\n"
    REPORT_MD.write_text(new_txt, encoding="utf-8")
    print("  Updated REPORT.md with chart gallery:", REPORT_MD)
else:
    print("  NOTE: No plots found to embed into REPORT.md")

print("[OK] Done.")
