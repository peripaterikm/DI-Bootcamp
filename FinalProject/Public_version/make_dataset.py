# make_dataset.py — ETL + EDA for Israeli Economy (fixed-path Windows version)
# I keep the script, raw Excel files, and outputs in the same folder tree.

from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import re
from datetime import datetime
import sys
import unicodedata

# ==== CONFIG ====
# I keep debug logs on until I'm fully happy with the parsing.
DEBUG = True
# Some official spreadsheets are messy; I lower the minimum date-parse success rate.
DATE_MIN_PARSE_FRAC = 0.20
# Minimum number of valid points required to treat a column as a time series.
MIN_VALID_POINTS = 6

# ==== FOLDERS (my local layout) ====
BASE  = Path(r"C:\DI-Bootcamp\FinalProject\AllTogether")
OUT   = BASE / "Out"
PLOTS = OUT / "plots"
OUT.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)

print(f"[INFO] Input folder : {BASE}")
print(f"[INFO] Output folder: {OUT}")

# ==== EXPECTED SOURCES (I match files by keywords in filename, case-insensitive) ====
EXPECTED = {
    "cpi_total":              ["consumer price index", "cpi"],
    "boi_policy_rate":        ["bank of israel nominal interest rate", "policy rate", "boi"],
    "unemployment_25_64":     ["unemployment", "25-64"],
    "real_wage":              ["average monthly real wages", "real wages", "wage"],
    "house_price_index_oecd": ["oecd_house_prices", "house prices", "hpi", "house_price"],
    "mortgage_volumes":       ["housing loans", "mortgage", "variable rate", "fixed rate"],
    "fx_rates":               ["exchange rates", "shekel", "ils", "usd", "eur", "gbp"],
    "gdp_growth_annual_terms":["gdp - rate of change", "gdp growth", "annual terms"],
    "dem_misc":               ["dem.xlsx"]  # optional / nice-to-have
}

# ==== HELPERS ====
def log(msg: str):
    if DEBUG:
        print(msg)

def normalize_text(s: str | float | int | None) -> str | None:
    """I normalize Unicode, strip RTL marks, trim, and collapse spaces."""
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    t = str(s)
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("\u200f", "").replace("\u200e", "")
    t = re.sub(r"\s+", " ", t.strip())
    return t

def read_excel_file(path: Path):
    """
    I prefer .xlsx. If a file is .xls and xlrd<2.0 is not installed, I skip it.
    """
    if path.suffix.lower() == ".xls":
        try:
            import xlrd  # noqa
        except Exception:
            print(f"[WARN] {path.name}: .xls without xlrd -> skipping (I'll convert to .xlsx if I need it).")
            raise
    return pd.ExcelFile(path)

def raw_header_guess(df_nohdr: pd.DataFrame) -> int:
    """
    I guess the header row as the row with the most non-empty cells.
    Works well for government spreadsheets with preface rows.
    """
    scores = df_nohdr.apply(
        lambda r: r.astype(str).str.strip().replace({"nan": "", "None": ""}).ne("").sum(),
        axis=1
    )
    if scores.empty:
        raise ValueError("Empty sheet")
    return int(scores.idxmax())

def parse_dates_any(series: pd.Series) -> pd.Series:
    """
    I try multiple patterns: native datetime, generic parse, YYYY-Q#, YYYY-MM, or YYYY.
    Everything is coerced to Timestamp; unknowns become NaT.
    """
    s = series.copy()
    if pd.api.types.is_datetime64_any_dtype(s):
        return pd.to_datetime(s, errors="coerce")
    # 1) Generic parser
    d = pd.to_datetime(s, errors="coerce", infer_datetime_format=True)
    if d.notna().mean() >= DATE_MIN_PARSE_FRAC:
        return d
    # 2) Pattern-based parsing
    s_str = s.astype(str).str.strip()

    # YYYY-Q#
    m = s_str.str.extract(r"(?P<y>19\d{2}|20\d{2}).*?(?P<q>Q[1-4])")
    if m.notna().all(axis=1).any():
        y = pd.to_numeric(m["y"], errors="coerce")
        q = m["q"].str.extract(r"Q([1-4])").astype(float)[0]
        months = (q * 3).astype(int)  # quarter-end month: 3,6,9,12
        return pd.to_datetime(dict(year=y, month=months, day=1), errors="coerce")

    # YYYY-MM (or YYYY M)
    ym = s_str.str.extract(r"(?P<y>19\d{2}|20\d{2})\D(?P<m>[01]?\d)")
    if ym.notna().all(axis=1).any():
        y = pd.to_numeric(ym["y"], errors="coerce")
        m = pd.to_numeric(ym["m"], errors="coerce")
        return pd.to_datetime(dict(year=y, month=m, day=1), errors="coerce")

    # YYYY
    y = s_str.str.extract(r"(?P<y>19\d{2}|20\d{2})")
    if y.notna().any().any():
        y = pd.to_numeric(y[0], errors="coerce")
        return pd.to_datetime(dict(year=y, month=1, day=1), errors="coerce")

    return pd.to_datetime(pd.Series(index=s.index, dtype=float), errors="coerce")

def find_date_col(df: pd.DataFrame):
    """
    I scan columns and pick the one with the highest date-parse rate.
    If nothing reaches the threshold, I still return the best-effort column.
    """
    best_col, best_dt, best_frac = None, None, -1.0
    for c in df.columns:
        dt = parse_dates_any(df[c])
        frac = dt.notna().mean()
        if frac > best_frac:
            best_col, best_dt, best_frac = c, dt, frac
    return best_col, best_dt, float(best_frac)

def sanitize_value_series(col: pd.Series) -> pd.Series:
    """
    I clean numeric-like strings (%, thousand separators, RTL marks) and return floats.
    """
    s = col.copy()
    if s.dtype == object:
        s = s.astype(str)
        s = s.str.replace("%", "", regex=False)
        s = s.str.replace("\u200f", "", regex=False).str.replace("\u200e", "", regex=False)
        s = s.str.replace(",", "", regex=False)
    return pd.to_numeric(s, errors="coerce")

def canonical_name_from_file(file_key: str, raw_col: str, pos: int) -> tuple[str, str]:
    """
    I convert raw column names into human-friendly series IDs and display names.
    Mapping is mostly file-driven; column order helps disambiguate.
    """
    base = {
        "cpi_total":                ("cpi_total_index", "CPI Index — Total"),
        "boi_policy_rate":          ("boi_policy_rate_pct", "BOI Policy Rate (%)"),
        "unemployment_25_64":       ("unemployment_25_64_pct", "Unemployment Rate — Ages 25–64 (%)"),
        "real_wage":                ("real_wage_avg_monthly", "Average Monthly Real Wage"),
        "house_price_index_oecd":   ("house_price_index", "House Price Index (OECD)"),
        "gdp_growth_annual_terms":  ("gdp_growth_annual_terms_pct", "GDP Growth (annual terms, %)"),
    }
    if file_key in base and pos == 1:
        return base[file_key]

    if file_key == "mortgage_volumes":
        mapping = {
            1: ("mortgage_volume_total",    "Mortgage Volumes — Total"),
            2: ("mortgage_volume_variable", "Mortgage Volumes — Variable Rate"),
            3: ("mortgage_volume_fixed",    "Mortgage Volumes — Fixed Rate"),
        }
        return mapping.get(pos, (f"mortgage_volume_col{pos}", f"Mortgage Volume (col {pos})"))

    if file_key == "fx_rates":
        raw = str(raw_col).lower()
        if any(k in raw for k in ["usd", "dollar"]): return ("usd_ils", "USD/ILS")
        if any(k in raw for k in ["eur", "euro"]):   return ("eur_ils", "EUR/ILS")
        if any(k in raw for k in ["gbp", "pound"]):  return ("gbp_ils", "GBP/ILS")
        # If header is generic (e.g., "Unnamed"), I fall back to column order
        fallback = {1: ("usd_ils", "USD/ILS"), 2: ("eur_ils", "EUR/ILS"), 3: ("gbp_ils", "GBP/ILS")}
        return fallback.get(pos, (f"fx_col{pos}", f"FX series (col {pos})"))

    if file_key == "dem_misc":
        return (f"dem_col{pos}", f"DEM series (col {pos})")

    return (f"{file_key}_col{pos}", f"{file_key} (col {pos})")

def sanitize_series_name(series_id: str, series_name: str | None) -> str:
    """
    I ensure display names are clean English, even if the source used Russian or messy headers.
    """
    nid = (series_id or "").lower()
    name = normalize_text(series_name) or ""

    # Canonical overrides by known IDs
    canonical = {
        "cpi_total_index": "CPI Index — Total",
        "boi_policy_rate_pct": "BOI Policy Rate (%)",
        "unemployment_25_64_pct": "Unemployment Rate — Ages 25–64 (%)",
        "real_wage_avg_monthly": "Average Monthly Real Wage",
        "house_price_index": "House Price Index (OECD)",
        "mortgage_volume_total": "Mortgage Volumes — Total",
        "mortgage_volume_variable": "Mortgage Volumes — Variable Rate",
        "mortgage_volume_fixed": "Mortgage Volumes — Fixed Rate",
        "gdp_growth_annual_terms_pct": "GDP Growth (annual terms, %)",
        "usd_ils": "USD/ILS",
        "eur_ils": "EUR/ILS",
        "gbp_ils": "GBP/ILS",
    }
    if nid in canonical:
        return canonical[nid]

    nlo = name.lower()

    # Keyword heuristics (English + Russian)
    if any(k in nlo for k in ["consumer price index", "cpi", "индекс потреб", "индекс цен"]):
        return "CPI Index — Total"
    if any(k in nlo for k in ["policy rate", "boi", "ставка", "процентн"]):
        return "BOI Policy Rate (%)"
    if any(k in nlo for k in ["unemployment", "безработ"]):
        return "Unemployment Rate — Ages 25–64 (%)" if "25_64" in nid else "Unemployment Rate (%)"
    if any(k in nlo for k in ["wage", "зарплат", "заработн"]):
        return "Average Monthly Real Wage"
    if any(k in nlo for k in ["house price", "hpi", "жиль", "недвиж"]):
        return "House Price Index (OECD)"
    if any(k in nlo for k in ["mortgage", "housing loan", "ипотек"]):
        if "variable" in nlo or "перем" in nlo:
            return "Mortgage Volumes — Variable Rate"
        if "fixed" in nlo or "фикс" in nlo:
            return "Mortgage Volumes — Fixed Rate"
        return "Mortgage Volumes — Total"
    if any(k in nlo for k in ["gdp", "ввп"]):
        return "GDP Growth (annual terms, %)"
    if any(k in nlo for k in ["usd", "доллар"]):
        return "USD/ILS"
    if any(k in nlo for k in ["eur", "евро"]):
        return "EUR/ILS"
    if any(k in nlo for k in ["gbp", "фунт"]):
        return "GBP/ILS"

    # Fallback: title-case the cleaned original
    return name.title() if name else nid

def guess_frequency(dates: pd.Series) -> str:
    """
    I estimate frequency by looking at month deltas between unique timestamps.
    Using Period('M')->int keeps this robust across pandas versions (no .values needed).
    """
    d = pd.to_datetime(dates.dropna().unique())
    if len(d) < 4:
        return "unknown"
    months = pd.DatetimeIndex(d).to_period("M").astype(int)
    months = np.sort(months)
    diffs = np.diff(months)
    if diffs.size == 0:
        return "unknown"
    med = int(np.median(diffs))
    if med == 1:  return "monthly"
    if med == 3:  return "quarterly"
    if 11 <= med <= 13: return "annual"
    return "irregular"

def eda_checks(df_tidy: pd.DataFrame) -> pd.DataFrame:
    """
    I compute per-series quality stats: coverage, date range, freq guess, missing %, duplicate dates,
    extreme outliers (|z|>5), and huge MoM moves (>50%).
    """
    rows = []
    for sid, g in df_tidy.groupby("series_id"):
        dates = pd.to_datetime(g["date"])
        vals  = pd.to_numeric(g["value"], errors="coerce")
        n = len(g)
        missing = g["value"].isna().mean()*100
        dup_dates = dates.duplicated().sum()
        dr = (dates.min(), dates.max())
        freq = guess_frequency(dates)
        std = vals.std(ddof=0)
        z = (vals - vals.mean())/std if std not in [0, np.nan] else pd.Series([0]*len(vals))
        outliers = int((np.abs(z) > 5).sum())
        mom = vals.pct_change(1).abs()*100
        big_mom = int((mom > 50).sum())

        rows.append({
            "series_id": sid,
            "series_name": g["series_name"].iloc[0],
            "observations": n,
            "date_from": dr[0].date() if pd.notna(dr[0]) else None,
            "date_to": dr[1].date() if pd.notna(dr[1]) else None,
            "freq_guess": freq,
            "missing_pct": round(float(missing), 2),
            "duplicate_dates": int(dup_dates),
            "outliers_z_gt_5": outliers,
            "big_mom_moves_gt50pct": big_mom,
            "source_file": g["source_file"].iloc[0]
        })
    return pd.DataFrame(rows).sort_values(["source_file","series_id"])

def load_one(path: Path, file_key: str) -> list[pd.DataFrame]:
    """
    I read each sheet, auto-detect the header row, pick the best date column,
    keep numeric columns, attach canonical IDs/names, and return tidy chunks.
    In rescue mode I also try "first col = date, last col = value".
    """
    try:
        xls = read_excel_file(path)
    except Exception:
        return []

    out = []
    for sheet in xls.sheet_names:
        # 1) Read raw sheet with no header to guess the header row
        try:
            raw = pd.read_excel(path, sheet_name=sheet, header=None)
            if raw.empty:
                continue
        except Exception as e:
            log(f"[DBG] {path.name}::{sheet} failed to read raw: {e}")
            continue

        # 2) Guess header
        try:
            header_idx = raw_header_guess(raw)
        except Exception as e:
            log(f"[DBG] {path.name}::{sheet} header guess failed: {e}")
            continue

        # 3) Read with inferred header row
        try:
            df = pd.read_excel(path, sheet_name=sheet, header=header_idx)
        except Exception as e:
            log(f"[DBG] {path.name}::{sheet} failed to read with header={header_idx}: {e}")
            continue

        # 4) Drop empty rows/cols
        df = df.dropna(how="all").dropna(axis=1, how="all")
        if df.empty:
            log(f"[DBG] {path.name}::{sheet} empty after dropping null rows/cols")
            continue

        # 5) Identify the best date column
        date_col, dt, frac = find_date_col(df)
        if date_col is None:
            log(f"[DBG] {path.name}::{sheet} no date-like column found")
            continue
        df["__date__"] = dt
        log(f"[DBG] {path.name}::{sheet} header_idx={header_idx}, date_col='{date_col}', parsed={frac:.2f}")

        # 6) Collect numeric columns (coerce strings to floats)
        num_cols = []
        for c in df.columns:
            if c in ["__date__", date_col]:
                continue
            vals = sanitize_value_series(df[c])
            if vals.notna().sum() >= max(MIN_VALID_POINTS, int(len(vals)*0.10)):
                num_cols.append((c, vals))

        # 7) Rescue path: if nothing numeric detected, try "last column as values"
        if not num_cols and df.shape[1] >= 2:
            last_col = df.columns[-1]
            vals = sanitize_value_series(df[last_col])
            if vals.notna().sum() >= MIN_VALID_POINTS:
                num_cols.append((last_col, vals))
                log(f"[DBG] {path.name}::{sheet} rescue picked last column '{last_col}' as values")

        log(f"[DBG] {path.name}::{sheet} numeric_candidates={len(num_cols)}")

        # 8) Build tidy rows with sanitized English names
        pos = 0
        for c, vals in num_cols:
            pos += 1
            sid, sname = canonical_name_from_file(file_key, str(c), pos)
            sname = sanitize_series_name(sid, sname)
            d = pd.DataFrame({
                "date": df["__date__"],
                "series_id": sid,
                "series_name": sname,
                "value": vals,
                "source_file": path.name,
                "sheet": sheet
            }).dropna(subset=["date"]).sort_values("date")
            out.append(d)

    return out

def match_file(all_excel: list[Path], keywords: list[str]) -> Path | None:
    """
    I pick the first file whose name contains any of the keywords.
    I prioritize .xlsx over .xls to avoid xlrd dependency headaches.
    """
    keys = [k.lower() for k in keywords]
    candidates = sorted(all_excel, key=lambda p: (p.suffix.lower() != ".xlsx", p.name.lower()))
    for p in candidates:
        name = p.name.lower()
        if any(k in name for k in keys):
            return p
    return None

def to_markdown_fallback(df: pd.DataFrame) -> str:
    """
    I want a minimal Markdown table without relying on 'tabulate' if it's missing.
    """
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |",
           "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        cells = ["" if pd.isna(v) else str(v) for v in row]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)

def main():
    # Discover Excel files in the folder
    all_excel = [p for p in BASE.glob("*.*") if p.suffix.lower() in [".xlsx", ".xls"]]
    if not all_excel:
        print("[ERROR] No Excel files in the folder.")
        sys.exit(1)

    print("[INFO] Found files:")
    for p in all_excel:
        print("   -", p.name)

    # Map files to expected keys using simple keyword matching
    FILES = {}
    for k, kws in EXPECTED.items():
        f = match_file(all_excel, kws)
        if f is not None:
            FILES[k] = f
        else:
            print(f"[WARN] Not found for {k} (looked for: {kws})")

    # Load each mapped file and build tidy chunks
    tidy_parts = []
    for key, fpath in FILES.items():
        chunks = load_one(fpath, key)
        if not chunks:
            log(f"[DBG] {fpath.name}: no usable numeric series extracted")
        else:
            tidy_parts.extend(chunks)

    if not tidy_parts:
        print("No data collected.")
        sys.exit(1)

    # Finalize tidy dataframe
    tidy = pd.concat(tidy_parts, ignore_index=True)
    tidy["date"]  = pd.to_datetime(tidy["date"], errors="coerce")
    tidy["value"] = pd.to_numeric(tidy["value"], errors="coerce")

    # Drop near-empty series to avoid useless columns downstream
    keep = tidy.groupby("series_id")["value"].apply(
        lambda s: s.notna().sum() >= max(MIN_VALID_POINTS, int(len(s)*0.20))
    )
    tidy = tidy[tidy["series_id"].isin(keep[keep].index)].copy()

    # Run EDA checks
    eda = eda_checks(tidy)

    # Produce wide view keyed to month-start for easy use in Tableau/PowerBI
    tidy["_month"] = tidy["date"].dt.to_period("M").dt.to_timestamp()
    wide = tidy.pivot_table(index="_month", columns="series_id", values="value", aggfunc="last").sort_index()
    wide.index.name = "date"

    # Export series dictionary (id -> sanitized English name)
    series_dict = tidy.drop_duplicates("series_id").set_index("series_id")["series_name"].sort_index()

    # === EXPORTS ===
    tidy_out = OUT / "israel_economy_tidy.csv"
    wide_out = OUT / "israel_economy_wide.csv"
    eda_out  = OUT / "EDA_REPORT.md"
    dict_out = OUT / "series_dictionary.csv"

    tidy[["date","series_id","series_name","value","source_file","sheet"]].to_csv(tidy_out, index=False)
    wide.to_csv(wide_out)
    series_dict.to_csv(dict_out, header=["series_name"])

    # Write compact EDA markdown (use pandas.to_markdown if available, else fallback)
    lines = []
    lines.append(f"# EDA Report — Israeli Economy (generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})")
    lines.append("")
    lines.append("## Summary by series")
    lines.append("")
    try:
        md_table = eda.to_markdown(index=False)  # requires 'tabulate'
    except Exception:
        md_table = to_markdown_fallback(eda)
    lines.append(md_table)
    lines.append("")
    lines.append("## Notes")
    lines.append("- Dates are coerced to month-start in the wide export; original timestamps are preserved in tidy.")
    lines.append("- Series names are sanitized to English using canonical mappings and keyword heuristics.")
    lines.append("- Outliers flagged as |z| > 5; large MoM moves flagged if >50%.")
    lines.append("- If a .xls was skipped, I'll convert it to .xlsx and rerun.")
    eda_out.write_text("\n".join(lines), encoding="utf-8")

    print("\n[OK] Exported:")
    print("  ", tidy_out)
    print("  ", wide_out)
    print("  ", eda_out)
    print("  ", dict_out)

if __name__ == "__main__":
    main()
