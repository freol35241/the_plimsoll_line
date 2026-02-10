# Synthetic Example Pipeline

This pipeline generates synthetic data for the demonstration story "The Distribution of Fictional Values."

The data is entirely fictional — it exists to demonstrate the story pattern and interactive components used by The Plimsoll Line.

## Running

```bash
pip install -r requirements.txt
python generate.py      # Creates raw/synthetic.csv
python process.py       # Validates and cleans
python export.py        # Exports to static/data/synthetic-example/data.json
```

## Data Description

- **200 items** across 3 categories (Type A, Type B, Type C) and 3 size classes (Small, Medium, Large)
- Each item has a measured `value` in fictional units
- Within each (category, size_class) group, values span a 2–3× range with some outliers
- All data is synthetic and generated with a fixed random seed for reproducibility
