<script>
	import { base } from '$app/paths';

	let { title, description, date, slug } = $props();
</script>

<a href="{base}/{slug}" class="story-card">
	<article>
		<time datetime={date}>{new Date(date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</time>
		<h2>{title}</h2>
		<p>{description}</p>
	</article>
</a>

<style>
	.story-card {
		display: block;
		padding: 1.5rem 0;
		border-bottom: 1px solid var(--color-border);
		text-decoration: none;
		color: inherit;
	}

	.story-card:hover {
		text-decoration: none;
	}

	.story-card:hover h2 {
		color: var(--color-accent);
	}

	article {
		max-width: var(--content-width);
	}

	time {
		font-size: 0.8rem;
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	h2 {
		font-family: var(--font-serif);
		font-size: 1.35rem;
		font-weight: 700;
		margin: 0.35rem 0 0.4rem;
		line-height: 1.3;
		transition: color 0.15s;
	}

	p {
		font-size: 0.95rem;
		color: var(--color-text-muted);
		margin: 0;
		line-height: 1.5;
	}
</style>
