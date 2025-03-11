<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	// Props with default values
	let {
		width = 40,
		height = 40,
		x = -1,
		y = -1,
		strokeDasharray = 0,
		numSquares = 50,
		maxOpacity = 0.5,
		pathOpacity = 0.5,
		squareColor = 'primary', // Use DaisyUI primary color by default
		gridColor = 'primary', // Use DaisyUI primary color by default
		duration = 4,
		repeatDelay = 0.5,
		class: customClass = ''
	} = $props();

	// Define types for our data structures
	type SquareData = {
		id: number;
		pos: [number, number];
		visible: boolean;
		nextUpdateTime: number;
	};

	type Dimensions = {
		width: number;
		height: number;
	};

	// Component state with proper typing
	let containerRef: HTMLDivElement;
	let dimensions = $state<Dimensions>({ width: 0, height: 0 });
	let squares = $state<SquareData[]>([]);
	let uniqueId = Math.random().toString(36).substring(2, 9);
	let resizeObserver: ResizeObserver | null = null;
	let animationTimer: ReturnType<typeof setTimeout> | null = null;
	let initialized = false;

	// Get random position based on container dimensions
	function getPos(): [number, number] {
		return [
			Math.floor((Math.random() * dimensions.width) / width),
			Math.floor((Math.random() * dimensions.height) / height)
		];
	}

	// Generate initial squares with staggered start times
	function generateSquares(count: number): SquareData[] {
		const now = Date.now();
		return Array.from({ length: count }, (_, i) => ({
			id: i,
			pos: getPos(),
			visible: false,
			// Stagger initial appearance
			nextUpdateTime: now + i * 100
		}));
	}

	// Single animation function that manages all squares
	function animateSquares(): void {
		if (animationTimer !== null) {
			clearTimeout(animationTimer);
		}

		// Function to run animation loop
		const updateSquares = () => {
			const now = Date.now();
			let hasChanges = false;
			const updatedSquares = [...squares];

			// Process each square
			for (let i = 0; i < updatedSquares.length; i++) {
				const square = updatedSquares[i];

				// Check if it's time to update this square
				if (now >= square.nextUpdateTime) {
					hasChanges = true;

					if (square.visible) {
						// If visible, hide it and schedule position change
						square.visible = false;
						square.nextUpdateTime = now + repeatDelay * 1000;
					} else {
						// If hidden, show it with new position
						square.visible = true;
						square.pos = getPos();
						square.nextUpdateTime = now + duration * 1000;
					}
				}
			}

			// Only update state if changes were made
			if (hasChanges) {
				squares = updatedSquares;
			}

			// Continue animation loop
			animationTimer = setTimeout(updateSquares, 50); // Check every 50ms
		};

		// Start animation loop
		updateSquares();
	}

	// Initialize or update when dimensions change
	function handleDimensionsChange(newWidth: number, newHeight: number): void {
		const isInitializing = !initialized && newWidth > 0 && newHeight > 0;
		const hasSizeChanged =
			initialized &&
			(Math.abs(dimensions.width - newWidth) > 20 || Math.abs(dimensions.height - newHeight) > 20);

		if (isInitializing || hasSizeChanged) {
			dimensions = { width: newWidth, height: newHeight };
			squares = generateSquares(numSquares);

			if (!initialized) {
				animateSquares();
				initialized = true;
			}
		}
	}

	// Initialize on mount
	onMount(() => {
		// Setup resize observer
		resizeObserver = new ResizeObserver((entries) => {
			for (let entry of entries) {
				handleDimensionsChange(entry.contentRect.width, entry.contentRect.height);
			}
		});

		if (containerRef) {
			// Initialize with current dimensions
			const rect = containerRef.getBoundingClientRect();
			handleDimensionsChange(rect.width, rect.height);

			// Observe for future dimension changes
			resizeObserver.observe(containerRef);
		}
	});

	// Cleanup on destroy
	onDestroy(() => {
		// Clean up resize observer
		if (resizeObserver && containerRef) {
			resizeObserver.unobserve(containerRef);
			resizeObserver.disconnect();
		}

		// Clean up animation timer
		if (animationTimer !== null) {
			clearTimeout(animationTimer);
		}
	});
</script>

<div
	bind:this={containerRef}
	class={`pointer-events-none inset-0 w-full h-full overflow-hidden ${customClass}`}
	aria-hidden="true"
>
	<svg class="absolute inset-0 h-full w-full" xmlns="http://www.w3.org/2000/svg">
		<defs>
			<pattern
				id={`grid-pattern-${uniqueId}`}
				{width}
				{height}
				patternUnits="userSpaceOnUse"
				{x}
				{y}
			>
				<!-- Horizontal line -->
				<line
					x1="0"
					y1="0"
					x2={width}
					y2="0"
					stroke={`var(--color-${gridColor})`}
					stroke-width="1.5"
					opacity={pathOpacity}
				/>
				<!-- Vertical line -->
				<line
					x1="0"
					y1="0"
					x2="0"
					y2={height}
					stroke={`var(--color-${gridColor})`}
					stroke-width="1.5"
					opacity={pathOpacity}
				/>
			</pattern>
		</defs>
		<!-- Apply pattern to full SVG -->
		<rect width="100%" height="100%" fill={`url(#grid-pattern-${uniqueId})`} />

		<!-- Animated squares -->
		<svg {x} {y} class="overflow-visible">
			{#each squares as square (square.id)}
				<rect
					width={width - 1}
					height={height - 1}
					x={square.pos[0] * width + 1}
					y={square.pos[1] * height + 1}
					fill={`var(--color-${squareColor})`}
					stroke-width="0"
					opacity={square.visible ? maxOpacity : 0}
					style="transition: opacity {duration / 2}s ease-in-out;"
				/>
			{/each}
		</svg>
	</svg>
</div>
