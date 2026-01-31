<script>
	import { base } from '$app/paths';
</script>

<header class="site-header">
	<nav>
		<a href="{base}/" class="site-title">The Plimsoll Line</a>
		<a href="{base}/about">About</a>
	</nav>
</header>

<style>
	.site-header {
		border-bottom: 1px solid var(--color-border);
		padding: 1.25rem 1.5rem;
	}

	nav {
		max-width: var(--interactive-width);
		margin: 0 auto;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.site-title {
		font-family: var(--font-serif);
		font-size: 1.15rem;
		font-weight: 700;
		color: var(--color-text);
	}

	.site-title:hover {
		text-decoration: none;
		color: var(--color-accent);
	}

	nav a:last-child {
		font-size: 0.9rem;
		color: var(--color-text-muted);
	}

	nav a:last-child:hover {
		color: var(--color-accent);
	}
</style>
