"""Export processed synthetic data to JSON for the frontend.

Reads processed.csv and writes static/data/synthetic-example/data.json.
"""

import json
from datetime import date
from pathlib import Path

import pandas as pd

PROCESSED_FILE = Path(__file__).parent / "processed.csv"
EXPORT_DIR = Path(__file__).parent.parent.parent / "static" / "data" / "synthetic-example"


def main() -> None:
    df = pd.read_csv(PROCESSED_FILE)

    items = []
    for _, row in df.iterrows():
        items.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "size_class": row["size_class"],
            "value": round(float(row["value"]), 1),
            "year": int(row["year"]),
        })

    # Sort by ID for consistency
    items.sort(key=lambda x: x["id"])

    output = {
        "metadata": {
            "generated": date.today().isoformat(),
            "description": "Synthetic data for demonstration — fictional items with measured values across categories and size classes",
            "units": "fictional units",
            "source": "Generated synthetically (see pipelines/synthetic-example/)",
        },
        "items": items,
    }

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EXPORT_DIR / "data.json"

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Exported {len(items)} items → {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
