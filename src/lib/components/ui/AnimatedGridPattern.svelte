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
		pathOpacity = 0.2,
		duration = 4,
		repeatDelay = 0.5,
		className = ''
	} = $props();

	// Define types for our data structures
	type SquareData = {
		id: number;
		pos: [number, number];
		visible: boolean;
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
	let animationTimers: number[] = [];
	
	// Get random position based on container dimensions
	function getPos(): [number, number] {
		return [
			Math.floor((Math.random() * dimensions.width) / width),
			Math.floor((Math.random() * dimensions.height) / height)
		];
	}

	// Generate initial squares
	function generateSquares(count: number): SquareData[] {
		return Array.from({ length: count }, (_, i) => ({
			id: i,
			pos: getPos(),
			visible: false
		}));
	}

	// Start animations with staggered timing
	function startAnimations(): void {
		// Clear any existing timers
		cleanupTimers();
		
		// Animate each square with staggered delays
		squares.forEach((square, index) => {
			// Stagger the initial appearance
			const showTimer = setTimeout(() => {
				squares = squares.map(sq => 
					sq.id === index ? { ...sq, visible: true } : sq
				);
				
				// Schedule the square to disappear after duration
				const hideTimer = setTimeout(() => {
					squares = squares.map(sq => 
						sq.id === index ? { ...sq, visible: false } : sq
					);
					
					// Then change position and restart cycle
					const moveTimer = setTimeout(() => {
						squares = squares.map(sq => 
							sq.id === index ? { ...sq, pos: getPos(), visible: true } : sq
						);
						
						// Create ongoing cycle
						const cycleTimer = setInterval(() => {
							// First hide
							squares = squares.map(sq => 
								sq.id === index ? { ...sq, visible: false } : sq
							);
							
							// Then move and show again
							setTimeout(() => {
								squares = squares.map(sq => 
									sq.id === index ? { ...sq, pos: getPos(), visible: true } : sq
								);
							}, repeatDelay * 1000);
						}, (duration + repeatDelay) * 1000);
						
						animationTimers.push(cycleTimer);
					}, repeatDelay * 1000);
					
					animationTimers.push(moveTimer);
				}, duration * 1000);
				
				animationTimers.push(hideTimer);
			}, index * 100); // 100ms stagger between squares
			
			animationTimers.push(showTimer);
		});
	}
	
	// Clean up all animation timers
	function cleanupTimers(): void {
		animationTimers.forEach(timer => clearTimeout(timer));
		animationTimers = [];
	}

	// Handle dimension changes
	function handleDimensionsChange(newWidth: number, newHeight: number): void {
		// Only update if dimensions changed significantly
		if (Math.abs(dimensions.width - newWidth) > 20 || 
			Math.abs(dimensions.height - newHeight) > 20) {
			
			dimensions = { width: newWidth, height: newHeight };
			
			// Generate new squares with the new dimensions
			squares = generateSquares(numSquares);
			
			// Start animations
			startAnimations();
		}
	}

	// Initialize on mount
	onMount(() => {
		// Setup resize observer
		resizeObserver = new ResizeObserver((entries) => {
			for (let entry of entries) {
				handleDimensionsChange(
					entry.contentRect.width,
					entry.contentRect.height
				);
			}
		});

		if (containerRef) {
			// Initialize with current dimensions
			const rect = containerRef.getBoundingClientRect();
			dimensions = { width: rect.width, height: rect.height };
			
			// Generate initial squares and start animations
			squares = generateSquares(numSquares);
			startAnimations();
			
			// Then observe for future dimension changes
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
		
		// Clean up all animation timers
		cleanupTimers();
	});
</script>

<div
	bind:this={containerRef}
	class={`pointer-events-none absolute inset-0 h-full w-full ${className}`}
	aria-hidden="true"
>
	<svg
		class="absolute inset-0 h-full w-full fill-gray-400/30 stroke-gray-400/30"
		xmlns="http://www.w3.org/2000/svg"
	>
		<defs>
			<pattern
				id={`grid-pattern-${uniqueId}`}
				{width}
				{height}
				patternUnits="userSpaceOnUse"
				{x}
				{y}
			>
				<path
					d={`M.5 ${height}V.5H${width}`}
					fill="none"
					stroke="currentColor"
					stroke-width="0.5"
					stroke-dasharray={strokeDasharray}
					opacity={pathOpacity}
				/>
			</pattern>
		</defs>
		<rect width="100%" height="100%" fill={`url(#grid-pattern-${uniqueId})`} />
		<svg x={x} y={y} class="overflow-visible">
			{#each squares as square (square.id)}
				<rect
					width={width - 1}
					height={height - 1}
					x={square.pos[0] * width + 1}
					y={square.pos[1] * height + 1}
					fill="currentColor"
					stroke-width="0"
					opacity={square.visible ? maxOpacity : 0}
					style="transition: opacity {duration/2}s ease-in-out;"
				/>
			{/each}
		</svg>
	</svg>
</div>