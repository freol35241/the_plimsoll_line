# The Plimsoll Line

A spotlight on systemic behavior.

Each story spotlights systemic behavior using public data, made interactive so readers can explore and draw their own conclusions. The data was already there; what was missing was the framing.

Named after [Samuel Plimsoll](https://en.wikipedia.org/wiki/Samuel_Plimsoll), who in the 1870s put the spotlight on British shipowners overloading vessels — systemic behavior that was killing sailors. The painted line on the hull made the behavior visible to anyone who looked.

## Development

```bash
npm install
npm run dev
```

## Data Pipelines

Each story has a data pipeline in `stories/<story-slug>/`:

```bash
cd stories/synthetic-example
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
