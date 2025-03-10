<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css';
	import Navbar from '$lib/components/ui/Navbar.svelte';
	import { initTheme } from '$lib/theme';

	let { children } = $props();

	const currentYear = new Date().getFullYear();

	onMount(() => {
		// Initialize theme on client side
		initTheme();
	});
</script>

<div class="flex min-h-screen flex-col">
	<Navbar logo="AI Factory" githubUrl="https://github.com/angelsen/ai-factory" />

	<main class="flex-grow">
		let {children} = $props();
	</main>

	<footer class="footer footer-center bg-base-200 text-base-content p-4">
		<aside>
			<p>© {currentYear} - Fredrik Angelsen</p>
		</aside>
	</footer>
</div>
