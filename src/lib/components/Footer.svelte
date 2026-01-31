<script>
	import { base } from '$app/paths';
</script>

<footer class="site-footer">
	<nav>
		<a href="{base}/about">About</a>
		<span class="sep" aria-hidden="true">&middot;</span>
		<a href="https://github.com/freol35241" target="_blank" rel="noopener noreferrer">GitHub</a>
	</nav>
</footer>

<style>
	.site-footer {
		border-top: 1px solid var(--color-border);
		padding: 2rem 1.5rem;
		margin-top: 4rem;
	}

	nav {
		max-width: var(--interactive-width);
		margin: 0 auto;
		display: flex;
		justify-content: center;
		gap: 0.75rem;
		font-size: 0.85rem;
		color: var(--color-text-muted);
	}

	nav a {
		color: var(--color-text-muted);
	}

	nav a:hover {
		color: var(--color-accent);
	}

	.sep {
		user-select: none;
	}
</style>
