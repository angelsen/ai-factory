<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css';
	import Navbar from '$lib/components/ui/Navbar.svelte';
	import AnimatedGridPattern from '$lib/components/ui/AnimatedGridPattern.svelte';
	import Footer from '$lib/components/ui/Footer.svelte';
	import { initTheme } from '$lib/theme';

	let { children } = $props();

	onMount(() => {
		// Initialize theme on client side
		initTheme();
	});
</script>

<div class="relative flex min-h-screen flex-col overflow-x-hidden">
	<!-- Global background pattern -->
	<AnimatedGridPattern
		numSquares={30}
		maxOpacity={0.5}
		pathOpacity={0.3}
		duration={3}
		repeatDelay={1}
		squareColor="secondary"
		gridColor="primary"
		class="absolute -z-10 [mask-image:radial-gradient(70%_70%_at_center,white,transparent)] inset-x-0 inset-y-[-30%] h-[200%] skew-y-12"
	/>
	<Navbar logo="AI Factory" githubUrl="https://github.com/angelsen/ai-factory" />

	<main class="flex-grow">
		{@render children()}
	</main>

	<Footer />
</div>
