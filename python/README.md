# Python Data Preparation Layer (Optional)

This folder is an **optional addition** to the Equity Investment Analysis
Dashboard. It does not change, replace, or automate the existing Power BI
dashboard in any way — it is a standalone demonstration of how the project's
data preparation *could* be scripted and eventually scheduled.

**The Power BI dashboard is unaffected.** It continues to read
`Dataset/Equity Investment Dataset.xlsx` exactly as before, using a fixed,
historical data snapshot. It is **not real-time and does not use live NSE
data** — nothing in this folder changes that.

## Purpose

The rest of the project shows the analysis and BI side of the work. This
folder shows a small, complementary data-engineering skill: reading raw
financial data, validating it, cleaning it, and producing a standardized
output — the kind of step that would sit in front of a dashboard in a
production setting.

## Data flow

```
Dataset/Equity Investment Dataset.xlsx  (existing, unchanged)
              │
              ▼
      python/data_cleaning.py
   (load → validate → dedupe → clean)
              │
              ▼
      python/data_pipeline.py
        (entry point, runs the
         above for all 3 sheets)
              │
              ▼
   python/output/*.csv  (new, generated)
   company_master_clean.csv
   financial_history_clean.csv
   shareholding_clean.csv
```

The source workbook has three sheets with different schemas, so the pipeline
produces three separate cleaned CSVs — one per sheet — rather than merging
them into one file. Column names are kept the same as the source wherever
possible so the outputs stay recognizable against the original dataset.

## How to run it

```bash
cd python
pip install -r requirements.txt
python data_pipeline.py
```

This will:
1. Load each of the three sheets from `../Dataset/Equity Investment Dataset.xlsx`.
2. Validate that expected columns are present.
3. Trim whitespace, drop exact duplicate rows, and drop any row missing its
   key identifier (e.g. a company name).
4. Convert numeric-looking columns to numeric types; leave genuinely missing
   values as missing rather than guessing a value.
5. Write cleaned CSVs to `python/output/`.
6. Print a summary: rows in/out, duplicates dropped, rows dropped, and any
   remaining missing values per sheet.

## What it does not do

- It does not modify `Dataset/Equity Investment Dataset.xlsx` or the `.pbix`
  file.
- It does not connect to Power BI automatically. If you wanted to point the
  dashboard at these CSVs instead of the Excel workbook, that would be a
  manual, separate change to the Power Query source step in Power BI —
  something this project deliberately has not done, to keep the existing
  dashboard exactly as-is.
- It does not pull live data by default. `data_source_optional.py` contains
  one clearly-separated, optional example of how a public financial-data API
  lookup *could* be added later; it is not called by `data_pipeline.py` and
  requires no credentials to leave the rest of the pipeline working.

## How this could eventually support periodic/automated refresh

If this were extended further, the natural next steps would be:
- Point `data_pipeline.py` at a refreshed source file (e.g. an updated
  export from NSE/Screener.in) on a schedule (cron, Task Scheduler, or a
  CI job).
- Optionally replace the manual Excel export step with a real API call via
  `data_source_optional.py`, once a specific data provider and credentials
  are chosen.
- Point Power BI's Power Query source at `python/output/*.csv` instead of
  the raw workbook, so each scheduled run refreshes the dashboard's input.

None of this is implemented — it's a documented pathway, not a running
system. The project's current, truthful state is: a fixed-snapshot Power BI
dashboard, plus a separate script that demonstrates how the data-prep step
could be automated later.

## What you can accurately say about this in a viva/interview

Accurate:
> "I explored and implemented a small Python-based data ingestion and
> preprocessing layer alongside the dashboard, to standardize and validate
> the financial data and show a pathway toward periodic automated updates.
> The dashboard itself still uses a fixed, historical data snapshot."

Not accurate — avoid saying:
- "Real-time stock market dashboard"
- "Live NSE integration"
- "Live financial data feed"

The dashboard's value is the BI/analysis work; this folder is evidence of
an additional, honestly-scoped technical skill on top of that.
