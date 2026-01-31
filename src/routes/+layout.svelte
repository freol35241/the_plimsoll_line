<script>
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import '$lib/styles/theme.css';

	let { children } = $props();
</script>

<div class="site">
	<Header />
	<main>
		{@render children()}
	</main>
	<Footer />
</div>

<style>
	.site {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	main {
		flex: 1;
		padding-top: 2rem;
		padding-bottom: 2rem;
	}
</style>
