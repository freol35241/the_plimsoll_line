<script>
	import StoryCard from '$lib/components/StoryCard.svelte';

	const stories = [
		{
			title: 'The Distribution of Fictional Values',
			description: 'Synthetic data reveals a 2–3× spread in measured values within peer groups — a pattern worth exploring.',
			date: '2025-01-15',
			slug: 'synthetic-example'
		}
	];
</script>

<svelte:head>
	<title>The Plimsoll Line</title>
</svelte:head>

<section class="landing">
	<div class="intro">
		<h1>The Plimsoll Line</h1>
		<p class="tagline">Data stories that reveal something worth reflecting over.</p>
	</div>

	<div class="stories">
		{#each stories as story}
			<StoryCard {...story} />
		{/each}
	</div>
</section>

<style>
	.landing {
		max-width: var(--content-width);
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}

	.intro {
		margin-bottom: 3rem;
	}

	h1 {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
	}

	.tagline {
		font-size: 1.1rem;
		color: var(--color-text-muted);
		margin: 0;
	}
</style>
