<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css';
	import Navbar from '$lib/components/ui/Navbar.svelte';
	import AnimatedGridPattern from '$lib/components/ui/AnimatedGridPattern.svelte';
	import { initTheme } from '$lib/theme';

	let { children } = $props();

	const currentYear = new Date().getFullYear();

	onMount(() => {
		// Initialize theme on client side
		initTheme();
	});
</script>

<div class="relative flex min-h-screen flex-col overflow-hidden">
	<!-- Global background pattern -->
	<AnimatedGridPattern
		numSquares={30}
		maxOpacity={0.5}
		pathOpacity={0.3}
		duration={3}
		repeatDelay={1}
		squareColor="secondary"
		gridColor="primary"
		className="absolute -z-10 [mask-image:radial-gradient(70%_70%_at_center,white,transparent)] inset-x-0 inset-y-0 h-full skew-y-12"
	/>
	<Navbar logo="AI Factory" githubUrl="https://github.com/angelsen/ai-factory" />

	<main class="flex-grow">
		{@render children()}
	</main>

	<footer class="footer footer-center bg-base-100 text-base-content p-4">
		<aside>
			<p>© {currentYear} - Fredrik Angelsen</p>
		</aside>
	</footer>
</div>
