<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';

	let { data } = $props();

	let selectedCategory = $state('all');
	let selectedSize = $state('all');
	let searchQuery = $state('');
	let viewMode = $state('all');
	let hoveredItem = $state(null);
	let tooltipX = $state(0);
	let tooltipY = $state(0);

	let svgEl = $state(null);
	let containerEl = $state(null);
	let width = $state(900);
	const margin = { top: 30, right: 20, bottom: 50, left: 60 };
	const height = 500;

	const categories = ['all', 'Type A', 'Type B', 'Type C'];
	const sizeClasses = ['all', 'Small', 'Medium', 'Large'];

	let filteredItems = $derived.by(() => {
		if (!data) return [];
		let items = data.items;

		if (selectedCategory !== 'all') {
			items = items.filter((d) => d.category === selectedCategory);
		}
		if (selectedSize !== 'all') {
			items = items.filter((d) => d.size_class === selectedSize);
		}
		if (searchQuery.trim()) {
			const q = searchQuery.trim().toLowerCase();
			items = items.filter(
				(d) => d.name.toLowerCase().includes(q) || d.id.toLowerCase().includes(q)
			);
		}
		return items;
	});

	let groupKey = $derived(
		viewMode === 'peer'
			? (d) => `${d.category} / ${d.size_class}`
			: () => 'All items'
	);

	let groups = $derived.by(() => {
		const map = d3.group(filteredItems, groupKey);
		return Array.from(map.entries()).sort((a, b) => d3.ascending(a[0], b[0]));
	});

	let groupNames = $derived(groups.map((g) => g[0]));

	let yScale = $derived(
		d3.scaleBand().domain(groupNames).range([margin.top, height - margin.bottom]).padding(0.3)
	);

	let xExtent = $derived(
		d3.extent(filteredItems, (d) => d.value) || [0, 100]
	);

	let xScale = $derived(
		d3
			.scaleLinear()
			.domain([Math.max(0, xExtent[0] - 5), xExtent[1] + 5])
			.range([margin.left, width - margin.right])
	);

	function getJitteredPositions(items, groupName) {
		const bandY = yScale(groupName);
		const bandH = yScale.bandwidth();
		if (bandY === undefined) return [];

		// Sort by value for consistent beeswarm-like layout
		const sorted = [...items].sort((a, b) => a.value - b.value);
		const radius = Math.min(4, bandH / 6);
		const placed = [];

		for (const item of sorted) {
			const cx = xScale(item.value);
			let cy = bandY + bandH / 2;

			// Simple collision avoidance: offset vertically if overlapping
			let attempts = 0;
			let offset = 0;
			const step = radius * 1.1;

			while (attempts < 20) {
				const testY = bandY + bandH / 2 + offset;
				const collision = placed.some(
					(p) =>
						Math.abs(p.x - cx) < radius * 2.2 && Math.abs(p.y - testY) < radius * 2.2
				);
				if (!collision && testY > bandY + radius && testY < bandY + bandH - radius) {
					cy = testY;
					break;
				}
				attempts++;
				offset = attempts % 2 === 0 ? (attempts / 2) * step : -(Math.ceil(attempts / 2)) * step;
			}

			placed.push({ ...item, x: cx, y: cy, r: radius });
		}

		return placed;
	}

	let allPositions = $derived.by(() => {
		const positions = [];
		for (const [name, items] of groups) {
			positions.push(...getJitteredPositions(items, name));
		}
		return positions;
	});

	function handleMouseEnter(item, event) {
		hoveredItem = item;
		const rect = containerEl.getBoundingClientRect();
		tooltipX = event.clientX - rect.left;
		tooltipY = event.clientY - rect.top;
	}

	function handleMouseLeave() {
		hoveredItem = null;
	}

	function handleFocus(item, event) {
		hoveredItem = item;
		const circle = event.target;
		const rect = containerEl.getBoundingClientRect();
		const circleRect = circle.getBoundingClientRect();
		tooltipX = circleRect.left - rect.left + circleRect.width / 2;
		tooltipY = circleRect.top - rect.top;
	}

	function handleBlur() {
		hoveredItem = null;
	}

	onMount(() => {
		const observer = new ResizeObserver((entries) => {
			for (const entry of entries) {
				width = Math.min(entry.contentRect.width, 1000);
			}
		});
		if (containerEl) observer.observe(containerEl);
		return () => observer.disconnect();
	});
</script>

<div class="explorer" bind:this={containerEl}>
	<div class="controls">
		<div class="control-group">
			<label for="category-filter">Category</label>
			<select id="category-filter" bind:value={selectedCategory}>
				{#each categories as cat}
					<option value={cat}>{cat === 'all' ? 'All categories' : cat}</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<label for="size-filter">Size class</label>
			<select id="size-filter" bind:value={selectedSize}>
				{#each sizeClasses as size}
					<option value={size}>{size === 'all' ? 'All sizes' : size}</option>
				{/each}
			</select>
		</div>

		<div class="control-group">
			<label for="search-input">Search</label>
			<input
				id="search-input"
				type="text"
				bind:value={searchQuery}
				placeholder="Name or ID..."
			/>
		</div>

		<div class="control-group">
			<label for="view-toggle">View</label>
			<select id="view-toggle" bind:value={viewMode}>
				<option value="all">All together</option>
				<option value="peer">By peer group</option>
			</select>
		</div>
	</div>

	<div class="chart-area">
		<svg bind:this={svgEl} {width} {height} role="img" aria-label="Strip plot showing distribution of values across groups. Use filters above to explore.">
			<!-- X axis -->
			{#each xScale.ticks(8) as tick}
				<line
					x1={xScale(tick)}
					x2={xScale(tick)}
					y1={margin.top}
					y2={height - margin.bottom}
					stroke="var(--color-border)"
					stroke-dasharray="2,2"
				/>
				<text
					x={xScale(tick)}
					y={height - margin.bottom + 20}
					text-anchor="middle"
					font-size="12"
					fill="var(--color-text-muted)"
					font-family="var(--font-mono)"
				>
					{tick}
				</text>
			{/each}

			<text
				x={(margin.left + width - margin.right) / 2}
				y={height - 5}
				text-anchor="middle"
				font-size="13"
				fill="var(--color-text-muted)"
				font-family="var(--font-sans)"
			>
				Value (fictional units)
			</text>

			<!-- Y axis group labels -->
			{#each groupNames as name}
				<text
					x={margin.left - 10}
					y={(yScale(name) ?? 0) + yScale.bandwidth() / 2}
					text-anchor="end"
					dominant-baseline="central"
					font-size="12"
					fill="var(--color-text)"
					font-family="var(--font-sans)"
				>
					{name}
				</text>

				<!-- Group background -->
				<rect
					x={margin.left}
					y={yScale(name)}
					width={width - margin.left - margin.right}
					height={yScale.bandwidth()}
					fill="var(--color-interactive-bg)"
					rx="2"
				/>
			{/each}

			<!-- Data points -->
			{#each allPositions as item}
				<circle
					cx={item.x}
					cy={item.y}
					r={item.r}
					fill={hoveredItem?.id === item.id ? 'var(--color-accent)' : 'var(--color-accent-light)'}
					stroke={hoveredItem?.id === item.id ? 'var(--color-accent)' : 'none'}
					stroke-width="1.5"
					opacity={hoveredItem && hoveredItem.id !== item.id ? 0.4 : 0.85}
					tabindex="0"
					role="button"
					aria-label="{item.name} ({item.id}): {item.value} units, {item.category}, {item.size_class}"
					onmouseenter={(e) => handleMouseEnter(item, e)}
					onmouseleave={handleMouseLeave}
					onfocus={(e) => handleFocus(item, e)}
					onblur={handleBlur}
					style="cursor: pointer; outline: none; transition: opacity 0.15s, fill 0.15s;"
				/>
			{/each}
		</svg>

		{#if hoveredItem}
			<div
				class="tooltip"
				style="left: {tooltipX}px; top: {tooltipY - 10}px;"
				role="tooltip"
			>
				<strong>{hoveredItem.name}</strong>
				<span class="tooltip-id">{hoveredItem.id}</span>
				<span class="tooltip-value">{hoveredItem.value} units</span>
				<span class="tooltip-meta">{hoveredItem.category} &middot; {hoveredItem.size_class}</span>
			</div>
		{/if}
	</div>

	<div class="summary">
		<p>
			Showing <strong>{filteredItems.length}</strong> of {data.items.length} items
			{#if filteredItems.length > 0}
				&mdash; range: {d3.min(filteredItems, (d) => d.value)} to {d3.max(filteredItems, (d) => d.value)} units
				({(d3.max(filteredItems, (d) => d.value) / d3.min(filteredItems, (d) => d.value)).toFixed(1)}× spread)
			{/if}
		</p>
	</div>
</div>

<style>
	.explorer {
		position: relative;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 1.5rem;
	}

	.controls {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin-bottom: 1.5rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--color-border);
	}

	.control-group {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}

	.control-group label {
		font-size: 0.75rem;
		font-weight: 600;
		color: var(--color-text-muted);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.control-group select,
	.control-group input {
		font-family: var(--font-sans);
		font-size: 0.9rem;
		padding: 0.4rem 0.6rem;
		border: 1px solid var(--color-border);
		border-radius: 4px;
		background: var(--color-bg);
		color: var(--color-text);
	}

	.control-group input {
		width: 160px;
	}

	.control-group select:focus,
	.control-group input:focus {
		outline: 2px solid var(--color-accent);
		outline-offset: 1px;
	}

	.chart-area {
		position: relative;
		overflow: hidden;
	}

	svg {
		display: block;
		width: 100%;
		height: auto;
	}

	.tooltip {
		position: absolute;
		pointer-events: none;
		background: var(--color-text);
		color: var(--color-bg);
		padding: 0.5rem 0.75rem;
		border-radius: 4px;
		font-size: 0.8rem;
		line-height: 1.4;
		transform: translate(-50%, -100%);
		white-space: nowrap;
		z-index: 10;
		display: flex;
		flex-direction: column;
	}

	.tooltip strong {
		font-weight: 600;
	}

	.tooltip-id {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		opacity: 0.7;
	}

	.tooltip-value {
		font-family: var(--font-mono);
		color: var(--color-accent-light);
	}

	.tooltip-meta {
		font-size: 0.75rem;
		opacity: 0.7;
	}

	.summary {
		margin-top: 1rem;
		padding-top: 0.75rem;
		border-top: 1px solid var(--color-border);
	}

	.summary p {
		font-size: 0.85rem;
		color: var(--color-text-muted);
		margin: 0;
		font-family: var(--font-mono);
	}

	@media (max-width: 640px) {
		.controls {
			flex-direction: column;
		}

		.control-group input {
			width: 100%;
		}

		.explorer {
			padding: 1rem;
		}
	}
</style>
