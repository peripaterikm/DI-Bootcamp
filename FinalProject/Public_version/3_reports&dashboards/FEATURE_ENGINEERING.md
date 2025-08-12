# Feature Engineering Report — Israel Macro Dashboard
_Generated: 2025-08-11 15:01 UTC_

## Goal
Turn the cleaned **wide** dataset into decision-ready indicators for analysis and a dashboard. Focus on momentum, policy stance, affordability, and composite risk signals.

## Inputs
- `israel_economy_wide.csv` (monthly index, one column per series_id)
- Key base series used:
  - CPI index (`cpi_total_index`)
  - BOI policy rate (`boi_policy_rate_pct`)
  - Unemployment 25–64 (`unemployment_25_64_pct`)
  - Real wage (`real_wage_avg_monthly`)
  - House Price Index (`house_price_index`)
  - Mortgage volume, total (`mortgage_volume_total`)
  - USD/ILS (`usd_ils`) and optional EUR/ILS (`eur_ils`)
  - GDP growth (annual terms, `gdp_growth_annual_terms_pct`)

## Derived Metrics (what & why)
- **CPI YoY (%)** = 12-month % change of CPI. _Inflation momentum; core policy input._
- **Real policy rate (%)** = Policy rate − CPI YoY. _Policy stance after inflation (tight vs. loose)._
- **Rate gap (p.p.)** = Policy rate − 2%. _Distance from target; simple tightening/easing proxy._
- **Rate change 12m (p.p.)** = Rate − Rate.shift(12). _Speed/scale of the cycle; credit sensitivity._
- **Real wage indexed (100=first obs)** = Real wage rebased to 100. _Clean view of living standards._
- **Wage growth 12m (%)** = 12-month % change of real wage. _Demand pressure; wage–price dynamics._
- **HPI total (level)** = Base HPI series. _Housing benchmark for YoY/affordability._
- **HPI indexed (100=first obs)** = HPI rebased to 100. _Comparable to wages and other indexed series._
- **HPI growth 12m (%)** = 12-month % change of HPI. _Housing price momentum._
- **Affordability (index)** = (Real wage index / HPI index) × 100. _Household ability to buy; higher is better._
- **FX change 12m (%)** = 12-month % change of USD/ILS. _Pass-through to prices; stress proxy._
- **FX MoM (%)** = 1-month % change of USD/ILS. _Short-term currency pulse._
- **FX volatility 12m** = Rolling 12-month std of FX MoM. _Currency instability; financial conditions._
- **CPI MoM (%)** = 1-month % change of CPI level. _Near-term inflation pulse._
- **Inflation volatility 12m** = Rolling 12-month std of CPI MoM. _Noise/uncertainty around inflation._
- **CPI gap (p.p.)** = CPI YoY − 2%. _Over/undershoot vs. target; policy signal._
- **Housing loans YoY (%)** = 12-month % change of mortgage volume. _Credit impulse into housing._
- **Economic stress index (z-score)** = mean of z-scores: `cpi_gap`, `fx_volatility_12m`, `unemp`, `rate_change_12m`, and `−gdp_growth`. _One dial for macro/financial strain._
- **Housing pressure index (z-score)** = mean of z-scores: `hpi_growth_12m`, `housing_loans_yoy`, and `−affordability`. _Heat in the housing market._

## Method & Handling
- All changes are computed on monthly data; YoY uses 12-period change, MoM uses 1-period change.
- Indexing to 100 uses the first valid observation of each series.
- Rolling windows use **12 months**. Z-scores standardize each component before averaging.
- No forward-fill or interpolation is applied; metrics respect data availability.
- Types are coerced to numeric; invalid values are dropped during calculations.

## Outputs
- `israel_economy_core_enhanced.csv` — base series + all derived metrics.
- PNG charts (in `Out/plots/`): CPI YoY, BOI rate, USD/ILS, Unemployment, Real wage (index), HPI YoY, Mortgage YoY, GDP growth, Real policy rate, Affordability, **Economic Stress**, **Housing Pressure**.
- `CORE_SUMMARY.md` — latest readings snapshot.

## Next
Use the core file to build the Tableau / Power BI dashboard (one page, time filter, rich tooltips: latest & YoY Δ).