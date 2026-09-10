"""
data_cleaning.py
-----------------
Cleaning / validation helpers for the Equity Investment Analysis Dashboard's
source workbook (Dataset/Equity Investment Dataset.xlsx).

This module is deliberately simple: it does NOT change the existing dataset,
DAX, or Power BI model. It reads the same workbook Power BI already uses and
produces cleaned, validated copies as separate CSV files for an optional
automation pathway (see python/README.md).

Each of the three source sheets is handled independently because they have
different schemas:
    - Company_Master   : one row per company, wide set of fundamentals
    - Financial Histroy : one row per (company, fiscal year)
    - Shareholding      : one row per company, ownership percentages

Design choices (kept intentionally simple, no ML/heavy validation frameworks):
    - Column names are kept as close to the source as possible. Only
      whitespace is trimmed; we do not rename columns, so the cleaned CSVs
      stay recognizable against the source workbook.
    - Missing numeric values are left as NaN (not silently zero-filled) and
      counted in the summary, since silently inventing financial figures
      would be misleading for an investment dataset.
    - Missing text/categorical values (Company, Sector, etc.) cause the row
      to be flagged; rows missing their key identifier (Company) are dropped
      since they cannot be joined to anything else.
    - Exact duplicate rows (all columns identical) are removed.
"""

from dataclasses import dataclass, field
import pandas as pd


# Sheets and the column that uniquely identifies a row within that sheet.
# "Financial Histroy" keeps the source's original (misspelled) sheet name so
# the loader points at the exact same tab Power BI reads from.
SHEET_KEY_COLUMNS = {
    "Company_Master": ["Company"],
    "Financial Histroy": ["Company", "FY"],
    "Shareholding": ["Company"],
    "Sheet4": ["Company"],
}

REQUIRED_COLUMNS = {
    "Company_Master": [
        "Company", "NSE Symbol", "Sector", "Industry", "Market Cap in crs.",
        "CMP", "PE", "PB", "EPS in rs", "ROE (%age)", "ROCE (%age)",
        "OPM (%age)", "Debt/Equity", "Revenue", "Net Profit",
        "Dividend Yield (%age)", "52W High", "52W Low", "1Y Return (%age)",
    ],
    "Financial Histroy": ["Company", "FY", "Revenue", "Profit"],
    "Shareholding": ["Company", "Promoter %", "FII %", "DII %", "Public %"],
    # "Sheet4" holds the Altman Z-Score inputs/outputs behind the
    # Financial Health dashboard page.
    "Sheet4": [
        "Company", "Working Capital", "Retained Earnings", "EBIT",
        "Market cap", "total Borrowings", "other liabilities",
        "total liabilities", "Revenue", "total Assets",
        "X1", "X2", "X3", "X4", "X5", "Z Score", "Risk Zone",
    ],
}

# Columns that must be present and non-null for a row to be usable at all.
CRITICAL_COLUMNS = {
    "Company_Master": ["Company"],
    "Financial Histroy": ["Company", "FY"],
    "Shareholding": ["Company"],
    "Sheet4": ["Company"],
}

# Columns that should never be negative for a real company (used for
# lightweight sanity-check warnings, not for dropping rows).
NON_NEGATIVE_COLUMNS = {
    "Sheet4": ["Market cap", "total liabilities", "total Assets", "Revenue"],
}


@dataclass
class SheetCleaningResult:
    """Summary of what happened when cleaning one sheet."""
    sheet_name: str
    rows_in: int
    rows_out: int
    duplicates_dropped: int
    rows_dropped_missing_key: int
    missing_value_counts: dict = field(default_factory=dict)
    missing_expected_columns: list = field(default_factory=list)
    negative_value_warnings: dict = field(default_factory=dict)

    def is_valid(self) -> bool:
        """A sheet is considered valid if no expected columns are missing
        and at least one row survived cleaning."""
        return not self.missing_expected_columns and self.rows_out > 0


def load_sheet(xlsx_path: str, sheet_name: str) -> pd.DataFrame:
    """Load a single sheet from the source workbook as-is (no cleaning)."""
    return pd.read_excel(xlsx_path, sheet_name=sheet_name)


def validate_columns(df: pd.DataFrame, sheet_name: str) -> list:
    """Return a list of expected columns that are missing from df."""
    expected = REQUIRED_COLUMNS.get(sheet_name, [])
    return [col for col in expected if col not in df.columns]


def clean_sheet(df: pd.DataFrame, sheet_name: str) -> SheetCleaningResult:
    """
    Clean one sheet in place-safe fashion (returns a new DataFrame via the
    caller's df.copy() pattern is left to the caller; this function mutates
    a local copy only) and returns both the cleaned DataFrame and a summary.

    Steps, in order:
        1. Trim whitespace from column names and from string cell values.
        2. Check for missing expected columns (recorded, not fatal).
        3. Drop exact duplicate rows.
        4. Drop rows missing a critical identifying column.
        5. Coerce obviously numeric columns to numeric dtype where possible.
        6. Count remaining missing values per column (informational only).
    """
    rows_in = len(df)
    working = df.copy()

    # 1. Trim whitespace
    working.columns = [str(c).strip() for c in working.columns]
    for col in working.select_dtypes(include="object").columns:
        working[col] = working[col].apply(
            lambda v: v.strip() if isinstance(v, str) else v
        )

    # 2. Column validation (informational — does not stop the pipeline)
    missing_expected = validate_columns(working, sheet_name)

    # 3. Drop exact duplicates
    before = len(working)
    working = working.drop_duplicates()
    duplicates_dropped = before - len(working)

    # 4. Drop rows missing a critical identifying column
    critical = [c for c in CRITICAL_COLUMNS.get(sheet_name, []) if c in working.columns]
    before = len(working)
    if critical:
        working = working.dropna(subset=critical)
    rows_dropped_missing_key = before - len(working)

    # 5. Coerce numeric-looking columns (everything except known text columns).
    # Try the conversion; if the column genuinely isn't numeric, leave it as-is
    # rather than forcing it (avoids pandas' deprecated errors="ignore").
    text_columns = {"Company", "NSE Symbol", "Sector", "Industry"}
    for col in working.columns:
        if col in text_columns:
            continue
        try:
            working[col] = pd.to_numeric(working[col])
        except (ValueError, TypeError):
            pass

    # 6. Missing value counts (left as NaN by design — see module docstring)
    missing_counts = {
        col: int(working[col].isna().sum())
        for col in working.columns
        if working[col].isna().sum() > 0
    }

    # 7. Sanity-check warnings for values that shouldn't be negative
    # (e.g. total assets, market cap). These are flagged, not corrected or
    # dropped — a negative figure usually means a data-entry issue upstream
    # that a human should look at, not something Python should silently fix.
    negative_warnings = {}
    for col in NON_NEGATIVE_COLUMNS.get(sheet_name, []):
        if col in working.columns:
            negative_rows = working.index[working[col] < 0].tolist()
            if negative_rows:
                companies = working.loc[negative_rows, "Company"].tolist() \
                    if "Company" in working.columns else negative_rows
                negative_warnings[col] = companies

    result = SheetCleaningResult(
        sheet_name=sheet_name,
        rows_in=rows_in,
        rows_out=len(working),
        duplicates_dropped=duplicates_dropped,
        rows_dropped_missing_key=rows_dropped_missing_key,
        missing_value_counts=missing_counts,
        missing_expected_columns=missing_expected,
        negative_value_warnings=negative_warnings,
    )
    return working, result