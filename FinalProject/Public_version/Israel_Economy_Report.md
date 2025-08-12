# Israel Economy Overview (2011–2025)

**Generated:** 2025-08-12 17:30 UTC

---

## Executive Summary

I built a single, decision-ready view of Israel’s economy. The pain was fragmented data from OECD, CBS and BoI. I automated ingestion and cleaning, standardized everything to monthly frequency, and engineered indicators: **CPI YoY**, **real policy rate**, **affordability**, **HPI/Mortgage YoY**, **GDP growth**, and **USD/ILS**.

On the dashboard you can see: CPI peaked in **2023** and cooled toward target; the Bank of Israel hiked fast and now keeps policy **restrictive** — the real rate is positive. This cooled housing: mortgage volumes fell, HPI slowed, affordability improved a bit. **FX is the swing risk.**

**Who uses this?** Financial teams, housing and credit professionals, and data teams who need a reproducible dataset.

**Challenges** were messy headers, mixed formats and long histories; I solved them with automated parsing, strict types, and a **15-year data-source filter** in Tableau.

**Next:** add inflation expectations for ex-ante real rates, a composite heatmap, and scheduled refreshes.

**Bottom line:** one pipeline, one dashboard — faster and clearer decisions.

---

## 1) Topic & Data Collection

I picked a broad topic — a high-level review of Israel’s economy — and ran into fragmented sources, different formats, mixed languages, and inconsistent headers. I solved this by downloading time-series data from:

- **OECD Data Explorer** — <https://data-explorer.oecd.org/>
- **Israel Central Bureau of Statistics** — <https://www.cbs.gov.il/>
- **Bank of Israel Statistics** — <https://www.boi.org.il/en/economic-roles/statistics/>

All raw files were placed into one folder.

---

## 2) Building the Base Dataset

Automation with **`make_dataset.py`**:

- auto-discovered and read all Excel files in the folder;
- detected the header row and the date column on each sheet; normalized dates;
- cleaned values (removed `%`, thousand separators, stray/hidden chars) and converted to floats;
- standardized English names (stable `series_id` + readable `series_name`);
- kept only valid numeric series; dropped empty or too-short ones;
- produced two canonical datasets:
  - **tidy (long)**
  - **wide (monthly)** — no interpolation/forward-fill;
- ran basic EDA: date range, frequency guess (monthly/quarterly/annual), missing %, duplicate dates, large MoM jumps, outliers;
- saved: `israel_economy_tidy.csv`, `israel_economy_wide.csv`, `series_dictionary.csv`, `EDA_REPORT.md`.

I used the **wide** file for feature engineering and the dashboard.

---

## Feature Engineering Report — Israel Macro Dashboard

### Goal
Turn the cleaned **wide** dataset into decision-ready indicators for analysis and the dashboard. Focus on momentum, policy stance, affordability, and composite risk signals.

### Inputs
- `israel_economy_wide.csv` (monthly index; one column per `series_id`)

**Key base series**
- CPI index (`cpi_total_index`)
- BOI policy rate (`boi_policy_rate_pct`)
- Unemployment 25–64 (`unemployment_25_64_pct`)
- Real wage (`real_wage_avg_monthly`)
- House Price Index (`house_price_index`)
- Mortgage volume, total (`mortgage_volume_total`)
- USD/ILS (`usd_ils`) and (optionally) EUR/ILS (`eur_ils`)
- GDP growth (annual terms, `gdp_growth_annual_terms_pct`)

### Derived Metrics — what & why
- **CPI YoY (%)** = 12-month % change of CPI. *Inflation momentum; core policy input.*
- **Real policy rate (%)** = policy rate − CPI YoY. *Policy stance after inflation (tight vs. loose).*
- **Rate gap (p.p.)** = policy rate − 2%. *Distance from target; simple tightening/easing proxy.*
- **Rate change 12m (p.p.)** = rate − rate.shift(12). *Speed/scale of the cycle; credit sensitivity.*
- **Real wage indexed (100 = first obs).** *Living standards over time, rebased.*
- **Wage growth 12m (%).** *Demand pressure; wage–price dynamics.*
- **HPI total (level).** *Benchmark for YoY/affordability.*
- **HPI indexed (100 = first obs).** *Comparable to wages and other indices.*
- **HPI growth 12m (%).** *Housing price momentum.*
- **Affordability (index)** = (Real wage index / HPI index) × 100. *Higher is better.*
- **FX change 12m (%)** (USD/ILS). *Pass-through to prices; stress proxy.*
- **FX MoM (%)** and **FX volatility 12m** (rolling std of MoM). *Short-term pulse and instability.*
- **CPI MoM (%)** and **Inflation volatility 12m**. *Near-term pulse and uncertainty.*
- **CPI gap (p.p.)** = CPI YoY − 2%. *Over/undershoot vs target.*
- **Housing loans YoY (%).** *Credit impulse into housing.*
- **Economic stress index (z)** = mean of z-scores: `cpi_gap`, `fx_volatility_12m`, `unemp`, `rate_change_12m`, and `−gdp_growth`.
- **Housing pressure index (z)** = mean of z-scores: `hpi_growth_12m`, `housing_loans_yoy`, and `−affordability`.

### Method & Handling
- Monthly frequency throughout; YoY = 12-period change; MoM = 1-period change.
- Indexing to 100 uses the first valid observation.
- Rolling windows use **12 months**; z-scores standardize components before averaging.
- No forward-fill or interpolation; metrics respect data availability.
- Types are coerced to numeric; invalid rows are dropped during calculations.

### Outputs
- `israel_economy_core_enhanced.csv` — base series + all derived metrics.  
- PNG charts (in `Out/plots/`): CPI YoY, BOI rate, USD/ILS, Unemployment, Real wage (index), HPI YoY, Mortgage YoY, GDP growth, Real policy rate, Affordability, plus composites.  
- `CORE_SUMMARY.md` — latest readings snapshot.

---

## Findings from the Dashboard (2011–2025)

**Inflation (CPI YoY).** After several years near zero (2016–2020), CPI accelerated sharply in 2022, peaked in 2023, and cooled back toward the BoI target band (1–3%) through 2024–2025.

**Monetary policy (BoI).** The policy rate sat near zero until 2022, followed by a fast hiking cycle; the rate then stabilized at a higher plateau. With inflation falling, the **real policy rate** turned positive — a clearly restrictive stance that helped cool CPI.

**Labor market.** Unemployment (25–64) remains low by historical standards, rebounding quickly after the COVID shock and supporting household demand.

**Housing.** HPI YoY accelerated into 2022 and then slowed; mortgage volumes surged in 2021–2022 and cooled sharply as rates rose; **affordability** worsened during the upswing and modestly improved as prices cooled.

**Currency (USD/ILS).** The shekel weakened notably in 2023 (higher USD/ILS), adding imported-inflation pressure, and later partially retraced.

**Growth.** After the 2020 contraction, GDP growth rebounded strongly in 2021 and then moderated under tighter financial conditions and external shocks; recent readings look like modest, non-overheating growth.

---

## Who Will Use This

- **Financial teams** (policy watchers in banks/funds) — stance vs CPI target, real rate.  
- **Housing/credit professionals** — HPI and mortgage cycles, affordability.  
- **Data/product teams** — a reproducible dataset and indicators for modeling.

---

## Challenges & How I Solved Them

**Challenges**
1) Mixed formats, headers and languages across sources.  
2) Different frequencies and broken date columns.  
3) Noisy values (`%`, thousand separators, hidden chars).  
4) Long histories that broke titles/min–max years in Tableau.

**Solutions**
1) Auto header/date detection; robust cleaners; typed numeric coercion.  
2) Standardized to **monthly**; YoY/MoM only when valid.  
3) Stable `series_id` + readable names; series dictionary CSV.  
4) **Data Source Filter = last 15 years**; optional table-calcs for MIN/MAX in titles.

---

## Future Steps (realistic)

1) Add **inflation expectations** vs real rate.  
2) Add a **composite heatmap** of macro stress and housing pressure.  
3) Publish a refreshable notebook + scheduled export (CSV + PNGs).

---

## Summary Points

- Israel is past the **2022–2023 CPI peak** and is returning toward target.  
- Policy stance is **restrictive** (positive real rate); housing cooled; affordability slightly improved.  
- Mortgage volumes fell; HPI slowed; affordability ticked up.
- Priority shifts from inflation control to growth support.

---

## Conclusion

One pipeline, one dashboard: a clean, consistent view of Israel’s macro picture that speeds up judgement for policy, credit and markets.
