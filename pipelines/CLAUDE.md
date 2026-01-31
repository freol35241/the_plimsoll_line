# Data Pipeline Instructions

You are working on data pipelines for **The Plimsoll Line**.

## Purpose

Each pipeline fetches, cleans, and transforms raw data into the JSON format consumed by the frontend. Pipelines live in `pipelines/<story-slug>/` and export to `static/data/<story-slug>/`.

## Pipeline Structure

```
pipelines/<story-slug>/
├── README.md              # What this pipeline does, how to run it
├── raw/                   # Raw data (preserved as-is)
│   ├── <data files>       # Original downloaded/scraped files
│   └── SOURCE.md          # Where data came from, when, licensing
├── generate.py            # (optional) Generate synthetic data for testing
├── process.py             # Clean, transform, validate raw data
├── export.py              # Export final JSON for the frontend
└── requirements.txt       # Python dependencies
```

## Reproducibility

Pipelines must be fully reproducible:

1. **Raw data is preserved** — never modify files in `raw/`. If the source changes, download a new copy alongside the old one.
2. **SOURCE.md is mandatory** — every `raw/` folder must have a `SOURCE.md` documenting:
   - Where the data came from (URL, API, FOIA request, etc.)
   - When it was downloaded
   - License or terms of use
   - Any known issues or caveats
3. **No manual steps** — the entire pipeline should run with:
   ```bash
   pip install -r requirements.txt
   python process.py
   python export.py
   ```
4. **Deterministic output** — same input should produce identical output. Avoid relying on random seeds without fixing them. Sort output consistently.

## SOURCE.md Template

```markdown
# Data Source

## Origin
- **URL:** [link to source]
- **Downloaded:** YYYY-MM-DD
- **Method:** [manual download / API / scrape / FOIA]

## License
[License information or terms of use]

## Description
[What this data contains, what each field means]

## Known Issues
[Any caveats, missing data, quality concerns]
```

## Processing Standards (process.py)

- Read from `raw/`
- Output cleaned intermediate data (CSV or similar) if helpful
- Validate data quality:
  - Check for missing values
  - Check for outliers that might be data errors
  - Check for duplicate records
  - Print summary statistics to stdout
- Log any records dropped and why

## Export Standards (export.py)

- Read processed data
- Export to `../../static/data/<story-slug>/data.json`
- JSON structure must include a `metadata` block:
  ```json
  {
    "metadata": {
      "generated": "YYYY-MM-DD",
      "description": "What this dataset contains",
      "units": "unit description",
      "source": "Brief source attribution"
    },
    "items": [...]
  }
  ```
- Keep file sizes reasonable (under 1MB preferred, under 5MB maximum)
- Round floating-point numbers to reasonable precision
- Sort items consistently (by ID or name)

## Python Standards

- Python 3.10+
- Use `pandas` for data manipulation
- Use `json` standard library for export
- Use `pathlib` for file paths
- Include type hints for function signatures
- No notebooks — scripts only

## Validation

Before considering a pipeline complete:
- [ ] `SOURCE.md` documents the data origin
- [ ] `process.py` runs without errors
- [ ] `export.py` produces valid JSON
- [ ] Exported JSON has a `metadata` block
- [ ] File size is reasonable
- [ ] Numbers are sensible (no obviously wrong values)
- [ ] `README.md` explains how to run the pipeline
