"""Generate synthetic data for the example story.

Creates ~200 items across 3 categories and 3 size classes with
interesting value distributions: 2-3x spread within each peer group,
with some outliers.
"""

import csv
import random
from pathlib import Path

SEED = 42
OUTPUT = Path(__file__).parent / "raw" / "synthetic.csv"

CATEGORIES = ["Type A", "Type B", "Type C"]
SIZE_CLASSES = ["Small", "Medium", "Large"]

# Base value ranges per (category, size_class) — center and spread
# Designed so groups have distinct but overlapping ranges
GROUP_PARAMS: dict[tuple[str, str], tuple[float, float]] = {
    ("Type A", "Small"):  (25.0, 8.0),
    ("Type A", "Medium"): (45.0, 12.0),
    ("Type A", "Large"):  (70.0, 18.0),
    ("Type B", "Small"):  (30.0, 10.0),
    ("Type B", "Medium"): (55.0, 15.0),
    ("Type B", "Large"):  (85.0, 22.0),
    ("Type C", "Small"):  (20.0, 7.0),
    ("Type C", "Medium"): (40.0, 11.0),
    ("Type C", "Large"):  (65.0, 17.0),
}

# Name parts for generating fictional names
PREFIXES = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi",
    "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
    "Nova", "Apex", "Core", "Flux", "Helix", "Ion", "Nexus", "Orbit",
    "Pulse", "Quark", "Relay", "Spark", "Terra", "Unity", "Vortex", "Wave",
]

SUFFIXES = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
    "Nine", "Ten", "Prime", "Major", "Minor", "Plus", "Star",
]


def generate_items(rng: random.Random) -> list[dict]:
    """Generate ~200 items with interesting distributions."""
    items = []
    item_num = 0

    # Roughly 22 items per group (9 groups × 22 ≈ 198), plus a few outliers
    for cat in CATEGORIES:
        cat_letter = cat.split()[-1][0]  # A, B, or C
        for size in SIZE_CLASSES:
            center, spread = GROUP_PARAMS[(cat, size)]
            n_items = rng.randint(20, 24)

            for _ in range(n_items):
                item_num += 1
                item_id = f"{cat_letter}{item_num:03d}"

                # Most values from a normal-ish distribution
                if rng.random() < 0.08:
                    # ~8% chance of being an outlier (high)
                    value = center + spread * rng.uniform(1.5, 2.5)
                elif rng.random() < 0.08:
                    # ~8% chance of being an outlier (low)
                    value = center - spread * rng.uniform(1.0, 1.8)
                else:
                    # Normal spread
                    value = rng.gauss(center, spread * 0.4)

                # Ensure positive values
                value = max(value, center * 0.3)
                value = round(value, 1)

                # Generate a name
                prefix = rng.choice(PREFIXES)
                suffix = rng.choice(SUFFIXES)
                name = f"{prefix} {suffix}"

                items.append({
                    "id": item_id,
                    "name": name,
                    "category": cat,
                    "size_class": size,
                    "value": value,
                    "year": 2023,
                })

    return items


def main() -> None:
    rng = random.Random(SEED)
    items = generate_items(rng)

    # Sort by ID for consistency
    items.sort(key=lambda x: x["id"])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "category", "size_class", "value", "year"])
        writer.writeheader()
        writer.writerows(items)

    print(f"Generated {len(items)} items → {OUTPUT}")


if __name__ == "__main__":
    main()
