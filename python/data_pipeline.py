"""
data_pipeline.py
-----------------
Optional data-preparation entry point for the Equity Investment Analysis
Dashboard project.

WHAT THIS DOES
    Reads the existing source workbook (../Dataset/Equity Investment
    Dataset.xlsx), validates and cleans each sheet, and writes cleaned CSV
    copies to python/output/. It prints a short summary of what happened.

WHAT THIS DOES NOT DO
    - It does not modify the source .xlsx or the .pbix in any way.
    - It does not connect the Power BI dashboard to these CSVs — the
      dashboard continues to use its existing fixed data snapshot exactly
      as it does today. Wiring these outputs into Power BI is a manual,
      optional step described in python/README.md, not something this
      script does automatically.
    - It is not a real-time or live data feed. It runs on demand, once,
      against a static workbook.

HOW TO RUN
    cd python
    pip install -r requirements.txt
    python data_pipeline.py
"""

import os
import sys
import logging

from data_cleaning import load_sheet, clean_sheet, SHEET_KEY_COLUMNS

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger("data_pipeline")

# Paths are relative to this file so the script works regardless of the
# directory it's invoked from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_XLSX = os.path.join(SCRIPT_DIR, "..", "Dataset", "Equity Investment Dataset.xlsx")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Maps source sheet name -> output CSV filename
OUTPUT_FILES = {
    "Company_Master": "company_master_clean.csv",
    "Financial Histroy": "financial_history_clean.csv",
    "Shareholding": "shareholding_clean.csv",
}


def run_pipeline(source_xlsx: str = SOURCE_XLSX, output_dir: str = OUTPUT_DIR) -> bool:
    """
    Run the full pipeline: load -> validate -> clean -> save -> summarize.
    Returns True if every sheet produced a valid, non-empty output.
    """
    if not os.path.exists(source_xlsx):
        logger.error("Source workbook not found: %s", source_xlsx)
        return False

    os.makedirs(output_dir, exist_ok=True)

    all_valid = True
    summaries = []

    for sheet_name, output_filename in OUTPUT_FILES.items():
        try:
            logger.info("Loading sheet: %s", sheet_name)
            raw_df = load_sheet(source_xlsx, sheet_name)
        except Exception as exc:  # noqa: BLE001 - keep this simple, log and continue
            logger.error("Failed to load sheet '%s': %s", sheet_name, exc)
            all_valid = False
            continue

        cleaned_df, result = clean_sheet(raw_df, sheet_name)
        summaries.append(result)

        if result.missing_expected_columns:
            logger.warning(
                "Sheet '%s' is missing expected columns: %s",
                sheet_name, result.missing_expected_columns,
            )

        out_path = os.path.join(output_dir, output_filename)
        cleaned_df.to_csv(out_path, index=False)
        logger.info("Wrote %s (%d rows)", out_path, len(cleaned_df))

        if not result.is_valid():
            all_valid = False

    _print_summary(summaries, output_dir)
    return all_valid


def _print_summary(summaries, output_dir: str) -> None:
    print("\n" + "=" * 60)
    print("DATA PIPELINE SUMMARY")
    print("=" * 60)
    for r in summaries:
        status = "OK" if r.is_valid() else "ISSUES FOUND"
        print(f"\nSheet: {r.sheet_name}  [{status}]")
        print(f"  Key column(s):            {SHEET_KEY_COLUMNS.get(r.sheet_name)}")
        print(f"  Rows in / rows out:        {r.rows_in} -> {r.rows_out}")
        print(f"  Duplicate rows dropped:    {r.duplicates_dropped}")
        print(f"  Rows dropped (missing key):{r.rows_dropped_missing_key}")
        if r.missing_expected_columns:
            print(f"  Missing expected columns:  {r.missing_expected_columns}")
        if r.missing_value_counts:
            print(f"  Remaining missing values:  {r.missing_value_counts}")
        else:
            print("  Remaining missing values:  none")
    print(f"\nOutput folder: {output_dir}")
    print("=" * 60)
    print("Note: this is a static, on-demand run against a fixed source")
    print("workbook. It does not change the existing Power BI dashboard.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run_pipeline()
    sys.exit(0 if ok else 1)
