# Frontend & Story Authoring Instructions

You are working on the SvelteKit frontend for **The Plimsoll Line**.

## Tech Stack

- SvelteKit 2 with Svelte 5
- Static adapter (no server-side logic)
- D3.js for data visualization
- TypeScript supported but not required (use `.svelte` and `.js` by default)

## Project Structure

```
src/
├── app.html                    # HTML shell
├── routes/
│   ├── +layout.svelte          # Shared shell (Header + Footer)
│   ├── +page.svelte            # Landing page (story list)
│   ├── about/
│   │   └── +page.svelte        # About page
│   └── <story-slug>/           # One folder per story
│       ├── +page.svelte        # Narrative page
│       └── Explorer.svelte     # Interactive component
└── lib/
    ├── components/
    │   ├── Header.svelte
    │   ├── Footer.svelte
    │   └── StoryCard.svelte
    └── styles/
        └── theme.css
```

## Story Page Pattern

Each story page follows this structure:

```svelte
<script>
  import Explorer from './Explorer.svelte';

  let data = $state(null);

  async function loadData() {
    const res = await fetch('/data/<story-slug>/data.json');
    data = await res.json();
  }

  $effect(() => { loadData(); });
</script>

<article class="prose">
  <h1>Story Title</h1>
  <p class="dateline">January 2025</p>

  <!-- Brief intro: what we're looking at -->
  <p>...</p>

  <!-- Key finding -->
  <p>...</p>
</article>

<!-- The interactive breaks out wider -->
<section class="wide">
  {#if data}
    <Explorer {data} />
  {/if}
</section>

<article class="prose">
  <!-- Brief closing -->
  <p>...</p>
</article>
```

Key points:
- Prose sections use `.prose` class (max 700px)
- Interactives use `.wide` class (max 1000px)
- Data is loaded client-side from `/data/<story-slug>/data.json`
- The interactive component is the main event — keep prose brief

## Interactive Component Pattern

Interactive components (e.g., `Explorer.svelte`) should:

1. Accept data as a prop
2. Handle their own filtering/interaction state internally
3. Use D3 for rendering (bindings to SVG or Canvas)
4. Be responsive (resize on window change)
5. Provide hover/focus details
6. Work with keyboard navigation

```svelte
<script>
  let { data } = $props();

  let selectedCategory = $state('all');
  let hoveredItem = $state(null);

  // D3 rendering logic...
</script>

<div class="explorer">
  <!-- Filter controls -->
  <!-- Visualization (SVG) -->
  <!-- Detail panel -->
</div>
```

## Component Guidelines

### Header
- Text-only: "The Plimsoll Line"
- Links to home and about
- Minimal, no logo

### Footer
- Links to about page and GitHub repo
- Subtle, doesn't compete with content

### StoryCard
- Title, one-sentence description, date
- Links to the story page
- Clean, typographic — no thumbnails or imagery

## Design System

### Colors
Use CSS custom properties defined in `theme.css`:
- `--color-bg` / `--color-surface` for backgrounds
- `--color-text` / `--color-text-muted` for text
- `--color-accent` for links and highlights (deep muted red)
- `--color-border` for subtle dividers
- `--color-interactive-bg` for chart/interactive backgrounds

### Typography
- Headlines: `var(--font-serif)` — Georgia
- Body: `var(--font-sans)` — system-ui
- Data/code: `var(--font-mono)` — ui-monospace
- Body line-height: 1.6+

### Layout
- Content width: 700px (`.prose`)
- Interactive width: 1000px (`.wide`)
- Generous vertical spacing

### Visual Principles
- Clean, lots of whitespace
- Typography-driven
- Muted palette with one accent
- No stock imagery or decorative illustrations
- Interactives are the visual centerpiece
- Mobile-friendly but desktop-first

## Accessibility Requirements

- All interactive elements must be keyboard-navigable
- SVG visualizations need appropriate ARIA labels
- Color is never the only way to distinguish data — use shape or position too
- Filter controls use proper `<label>` elements
- Hover details are also accessible via focus
- Minimum color contrast ratios (WCAG AA)
- Semantic HTML: `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`

## Data Loading

Stories load data from `static/data/<story-slug>/data.json` at runtime:

```js
const res = await fetch(`${base}/data/<story-slug>/data.json`);
const data = await res.json();
```

Import `base` from `$app/paths` when constructing URLs.
