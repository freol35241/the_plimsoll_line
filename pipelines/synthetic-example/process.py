"""Process and validate the synthetic example data.

Reads raw/synthetic.csv, validates data quality, and prints summary statistics.
For synthetic data this is mostly a demonstration of the pipeline pattern.
"""

import pandas as pd
from pathlib import Path

RAW_FILE = Path(__file__).parent / "raw" / "synthetic.csv"
PROCESSED_FILE = Path(__file__).parent / "processed.csv"


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Validate data quality and print diagnostics."""
    print(f"Total records: {len(df)}")
    print()

    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        print("WARNING: Missing values found:")
        print(missing[missing > 0])
    else:
        print("No missing values.")
    print()

    # Check for duplicates
    dupes = df.duplicated(subset=["id"]).sum()
    if dupes:
        print(f"WARNING: {dupes} duplicate IDs found.")
    else:
        print("No duplicate IDs.")
    print()

    # Summary statistics by group
    print("Value statistics by (category, size_class):")
    print("-" * 60)
    grouped = df.groupby(["category", "size_class"])["value"]
    stats = grouped.agg(["count", "min", "max", "mean", "std"])
    stats["spread"] = stats["max"] / stats["min"]
    print(stats.round(1).to_string())
    print()

    # Check for non-positive values
    non_positive = (df["value"] <= 0).sum()
    if non_positive:
        print(f"WARNING: {non_positive} non-positive values found.")
    else:
        print("All values are positive.")

    return df


def main() -> None:
    df = pd.read_csv(RAW_FILE)
    df = validate(df)

    # Write processed output (in this case identical to input, but
    # real pipelines would clean/transform here)
    df.to_csv(PROCESSED_FILE, index=False)
    print(f"\nProcessed data written to {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
