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
DATASET_DIR = os.path.join(SCRIPT_DIR, "..", "Dataset")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Maps source sheet name -> output CSV filename
OUTPUT_FILES = {
    "Company_Master": "company_master_clean.csv",
    "Financial Histroy": "financial_history_clean.csv",
    "Shareholding": "shareholding_clean.csv",
    "Sheet4": "financial_health_clean.csv",
}


def find_source_workbook(dataset_dir: str = DATASET_DIR) -> str:
    """
    Auto-detect the source workbook instead of hardcoding a filename.

    The dataset file has been renamed more than once during this project
    (Equity Investment Dataset.xlsx -> erdp__1_.xlsx -> back again), so
    instead of hardcoding a name that can silently go stale, this looks for
    whichever single .xlsx file currently sits in Dataset/. If there's more
    than one, it warns and picks the most recently modified one so a leftover
    old copy doesn't get read by mistake.
    """
    if not os.path.isdir(dataset_dir):
        raise FileNotFoundError(f"Dataset folder not found: {dataset_dir}")

    xlsx_files = [
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if f.lower().endswith(".xlsx") and not f.startswith("~$")  # skip Excel lock files
    ]

    if not xlsx_files:
        raise FileNotFoundError(f"No .xlsx file found in {dataset_dir}")

    if len(xlsx_files) > 1:
        xlsx_files.sort(key=os.path.getmtime, reverse=True)
        logger.warning(
            "Multiple .xlsx files found in %s: %s. Using the most recently "
            "modified one: %s. Consider removing the unused copies to avoid "
            "confusion about which file actually feeds Power BI.",
            dataset_dir,
            [os.path.basename(f) for f in xlsx_files],
            os.path.basename(xlsx_files[0]),
        )

    return xlsx_files[0]


def run_pipeline(source_xlsx: str = None, output_dir: str = OUTPUT_DIR) -> bool:
    """
    Run the full pipeline: find source -> load -> validate -> clean -> save
    -> summarize. Returns True if every sheet produced a valid, non-empty
    output.

    If source_xlsx isn't given, the workbook is auto-detected from
    Dataset/ (see find_source_workbook) rather than assuming a fixed name.
    """
    if source_xlsx is None:
        try:
            source_xlsx = find_source_workbook()
        except FileNotFoundError as exc:
            logger.error(str(exc))
            return False

    if not os.path.exists(source_xlsx):
        logger.error("Source workbook not found: %s", source_xlsx)
        return False

    logger.info("Using source workbook: %s", source_xlsx)
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
        if r.negative_value_warnings:
            print(f"  WARNING - negative values: {r.negative_value_warnings}")
    print(f"\nOutput folder: {output_dir}")
    print("=" * 60)
    print("Note: this is a static, on-demand run against a fixed source")
    print("workbook. It does not change the existing Power BI dashboard.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    ok = run_pipeline()
    sys.exit(0 if ok else 1)