# The Plimsoll Line

Data stories that reveal something worth reflecting over.

Each story uses public data, made interactive so readers can explore and draw their own conclusions. The editorial stance is revelation, not judgment — the data is the point.

Named after [Samuel Plimsoll](https://en.wikipedia.org/wiki/Samuel_Plimsoll), who in the 1870s used data and public outrage to force the marking of load lines on ships — a visible mark anyone could read.

## Development

```bash
npm install
npm run dev
```

## Data Pipelines

Each story has a data pipeline in `pipelines/<story-slug>/`:

```bash
cd pipelines/synthetic-example
pip install -r requirements.txt
python generate.py
python process.py
python export.py
```

Exported JSON lands in `static/data/<story-slug>/` and is loaded by the frontend at runtime.

## Deployment

Deployed to GitHub Pages on push to `main` via GitHub Actions. Uses SvelteKit's static adapter.

## License

MIT
