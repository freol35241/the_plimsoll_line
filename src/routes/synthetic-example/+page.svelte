<script>
	import { base } from '$app/paths';
	import Explorer from './Explorer.svelte';

	let data = $state(null);

	async function loadData() {
		const res = await fetch(`${base}/data/synthetic-example/data.json`);
		data = await res.json();
	}

	$effect(() => {
		loadData();
	});
</script>

<svelte:head>
	<title>The Distribution of Fictional Values — The Plimsoll Line</title>
</svelte:head>

<article class="prose">
	<header class="story-header">
		<time datetime="2025-01-15">January 15, 2025</time>
		<h1>The Distribution of Fictional Values</h1>
	</header>

	<p>
		How much variation should we expect within a group of similar things? If two items
		belong to the same category and the same size class, their measured values should
		be roughly comparable. In practice, the spread is wider than most people assume.
	</p>

	<p>
		This dataset contains 195 items across three categories and three size classes.
		Within each peer group — items of the same category and size — the highest
		measured value is typically 2 to 3 times the lowest. Some groups show even wider
		gaps.
	</p>

	<p>
		The interactive below shows every item in the dataset. Filter by category or
		size class to isolate peer groups, or search for a specific item. Hover over
		any point for details.
	</p>
</article>

<section class="wide">
	{#if data}
		<Explorer {data} />
	{:else}
		<div class="loading" aria-live="polite">Loading data&hellip;</div>
	{/if}
</section>

<article class="prose">
	<p>
		The variation within peer groups raises questions. Some of it may reflect genuine
		differences in the underlying properties of these items. Some may reflect
		measurement conditions. The data alone doesn't tell us which — but it does
		show that the range exists, and that it's substantial.
	</p>

	<p>
		This is synthetic data, created to demonstrate the pattern. In a real story, the
		items would be ships, factories, schools, or any population where peer comparison
		reveals something worth knowing.
	</p>
</article>

<style>
	.story-header {
		margin-bottom: 2rem;
	}

	.story-header time {
		display: block;
		font-size: 0.8rem;
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: 0.5rem;
	}

	.story-header h1 {
		margin: 0;
	}

	.loading {
		text-align: center;
		padding: 4rem 0;
		color: var(--color-text-muted);
	}

	section.wide {
		margin: 3rem auto;
	}
</style>
