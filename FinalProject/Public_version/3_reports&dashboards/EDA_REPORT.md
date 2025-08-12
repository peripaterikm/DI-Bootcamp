# EDA Report — Israeli Economy (generated 2025-08-11 13:47 UTC)

## Summary by series

| series_id                   | series_name                        |   observations | date_from   | date_to    | freq_guess   |   missing_pct |   duplicate_dates |   outliers_z_gt_5 |   big_mom_moves_gt50pct | source_file                                                                            |
|:----------------------------|:-----------------------------------|---------------:|:------------|:-----------|:-------------|--------------:|------------------:|------------------:|------------------------:|:---------------------------------------------------------------------------------------|
| real_wage_avg_monthly       | Average Monthly Real Wage          |            605 | 1975-01-01  | 2025-05-01 | monthly      |          0    |                 0 |                 0 |                       0 | Average monthly real wages per employee post - total.xlsx                              |
| boi_policy_rate_pct         | BOI Policy Rate (%)                |          11517 | 1994-01-27  | 2025-08-08 | irregular    |          0    |                 0 |                 0 |                       7 | Bank Of Israel nominal interest rate.xlsx                                              |
| mortgage_volume_total       | Mortgage Volumes — Total           |            168 | 2011-07-01  | 2025-06-01 | monthly      |          0    |                 0 |                 0 |                       3 | Business volumes - Housing Loans to Households  with variable rate and fixed rate.xlsx |
| cpi_total_index             | CPI Index — Total                  |            874 | 1952-09-01  | 2025-06-01 | monthly      |          0    |                 0 |                14 |                     100 | Consumer Price Index - Total.xlsx                                                      |
| dem_col1                    | Dem Series (Col 1)                 |            122 | 1970-01-01  | 1970-01-01 | unknown      |          0    |               121 |                 0 |                       0 | DEM.xlsx                                                                               |
| dem_col2                    | Dem Series (Col 2)                 |            122 | 1970-01-01  | 1970-01-01 | unknown      |          0    |               121 |                 0 |                       0 | DEM.xlsx                                                                               |
| gdp_growth_annual_terms_pct | GDP Growth (annual terms, %)       |            120 | 1995-04-01  | 2025-01-01 | quarterly    |          0    |                 0 |                 1 |                      72 | GDP - Rate of change in annual terms (GDP growth).xlsx                                 |
| eur_ils                     | EUR/ILS                            |           6272 | 2000-01-03  | 2025-08-08 | irregular    |          0.02 |                 0 |                 0 |                       0 | New Israeli shekel exchange rates.xlsx                                                 |
| gbp_ils                     | GBP/ILS                            |           6272 | 2000-01-03  | 2025-08-08 | irregular    |          0    |                 0 |                 0 |                       0 | New Israeli shekel exchange rates.xlsx                                                 |
| usd_ils                     | USD/ILS                            |           6272 | 2000-01-03  | 2025-08-08 | irregular    |          0.02 |                 0 |                 0 |                       0 | New Israeli shekel exchange rates.xlsx                                                 |
| house_price_index           | House Price Index (OECD)           |            125 | 1994-01-01  | 2025-01-01 | quarterly    |          0    |                 0 |                 0 |                       0 | OECD_HOUSE_PRICES.xlsx                                                                 |
| unemployment_25_64_pct      | Unemployment Rate — Ages 25–64 (%) |            162 | 2012-01-01  | 2025-06-01 | monthly      |          0    |                 0 |                 0 |                       0 | Unemployment rate - total 25-64.xlsx                                                   |

## Notes
- Dates are coerced to month-start in the wide export; original timestamps are preserved in tidy.
- Series names are sanitized to English using canonical mappings and keyword heuristics.
- Outliers flagged as |z| > 5; large MoM moves flagged if >50%.

## Data Processing Summary (what I did)

I downloaded time-series data from:
- OECD Data Explorer — https://data-explorer.oecd.org/
- Israel Central Bureau of Statistics — https://www.cbs.gov.il/
- Bank of Israel Statistics — https://www.boi.org.il/en/economic-roles/statistics/

I put all files into one folder and then:
- wrote `make_dataset.py` to find and read the Excel files automatically;
- detected the header row and the date column on each sheet, and normalized dates;
- cleaned values (removed `%`, thousand separators, hidden chars) and converted to floats;
- standardized series names in English (`series_id` + readable `series_name`);
- kept only valid numeric series; dropped empty or too-short ones;
- built two datasets: **tidy (long)** and **wide (monthly, no interpolation/forward-fill)**;
- ran basic EDA: date range, frequency guess (monthly/quarterly/annual), missing %, duplicate dates, big MoM jumps, and outliers;
- saved outputs: `israel_economy_tidy.csv`, `israel_economy_wide.csv`, `series_dictionary.csv`, `EDA_REPORT.md`.

Next, I use the wide file to compute metrics and build the dashboard.

## Data Processing Summary (what I did)

I downloaded time-series data from:
- OECD Data Explorer — https://data-explorer.oecd.org/
- Israel Central Bureau of Statistics — https://www.cbs.gov.il/
- Bank of Israel Statistics — https://www.boi.org.il/en/economic-roles/statistics/

I put all files into one folder and then:
- wrote `make_dataset.py` to find and read the Excel files automatically;
- detected the header row and the date column on each sheet, and normalized dates;
- cleaned values (removed `%`, thousand separators, hidden chars) and converted to floats;
- standardized series names in English (`series_id` + readable `series_name`);
- kept only valid numeric series; dropped empty or too-short ones;
- built two datasets: **tidy (long)** and **wide (monthly, no interpolation/forward-fill)**;
- ran basic EDA: date range, frequency guess (monthly/quarterly/annual), missing %, duplicate dates, big MoM jumps, and outliers;
- saved outputs: `israel_economy_tidy.csv`, `israel_economy_wide.csv`, `series_dictionary.csv`, `EDA_REPORT.md`.

Next, I use the wide file to compute metrics and build the dashboard.
