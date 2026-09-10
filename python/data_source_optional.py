"""
data_source_optional.py
------------------------
OPTIONAL, NOT USED BY THE MAIN PIPELINE BY DEFAULT.

This module is a small, illustrative example of how an external
financial-data API *could* be plugged into this project in the future to
support periodic/automated refresh of the source dataset. It is not wired
into data_pipeline.py, it is not run automatically, and it does not make
the Power BI dashboard "real-time" or "live" in any sense.

The existing dashboard continues to rely on the fixed historical snapshot
in Dataset/Equity Investment Dataset.xlsx. Nothing here changes that.

If you want to try this:
    - Some public quote endpoints work without an API key for basic
      lookups; others require a free API key you'd set as an environment
      variable (never hard-code credentials in this file).
    - This function is intentionally scoped to fetching a single quote for
      demonstration, not to replacing the dataset.

Example (illustrative only — requires the `requests` package and network
access, and is not exercised by the test/verification run of the main
pipeline):

    from data_source_optional import fetch_quote_example
    fetch_quote_example("TATASTEEL")
"""

import os


def fetch_quote_example(symbol: str) -> dict:
    """
    Illustrative example of an optional live-lookup function.

    Requires the `requests` package (see requirements.txt) and, depending
    on the provider you choose, an API key read from an environment
    variable (e.g. FINANCIAL_API_KEY) rather than being hard-coded here.

    This function is NOT called anywhere in data_pipeline.py. It exists to
    show a possible future extension path, as discussed in python/README.md
    under "How this could support periodic automated refresh".
    """
    try:
        import requests  # imported lazily so this optional module never
                          # breaks the main pipeline if requests isn't installed
    except ImportError as exc:
        raise ImportError(
            "The 'requests' package is required for fetch_quote_example(). "
            "Install it with: pip install requests"
        ) from exc

    api_key = os.environ.get("FINANCIAL_API_KEY")  # optional, provider-dependent
    if not api_key:
        raise RuntimeError(
            "No API key found in FINANCIAL_API_KEY environment variable. "
            "This is expected if you haven't configured an optional data "
            "provider — this function is not required for the pipeline "
            "or dashboard to work."
        )

    # Placeholder endpoint/shape — swap in a real provider's endpoint if
    # you choose to explore this further. Left unimplemented deliberately
    # so this repo never depends on a specific paid/rate-limited provider.
    raise NotImplementedError(
        "fetch_quote_example is a placeholder illustrating where an "
        "optional live lookup would go. Wire in a specific provider's "
        "endpoint here if you want to explore this further."
    )
