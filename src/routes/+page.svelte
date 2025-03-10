<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import { Rocket, FileText, Sparkles, ArrowRight } from '@lucide/svelte';
</script>

<div class="hero min-h-[calc(100vh-64px-56px)]">
	<div class="hero-content text-center">
		<div class="max-w-md">
			<div class="flex items-center justify-center gap-3 mb-2">
				<h1 class="text-5xl font-bold">AI Factory</h1>
				
				<div class="relative">
					<Sparkles 
						class="h-6 w-6 text-secondary" 
						strokeWidth={1.5} 
					/>
					<div class="absolute inset-0 rounded-full blur-md bg-secondary/30 -z-10 scale-150 animate-pulse"></div>
				</div>
			</div>
			
			<p class="py-6">
				Your unified platform for AI-powered workflows and data collection. Build, deploy, and scale
				with ease.
			</p>
			
			<div class="flex flex-col justify-center gap-2 sm:flex-row">
				<Button href="/demo" variant="primary" className="gap-2">
					<Rocket class="h-4 w-4" />
					Explore Demos
					<ArrowRight class="h-4 w-4" />
				</Button>
				<Button href="https://svelte.dev/docs/kit" variant="outline" className="gap-2">
					<FileText class="h-4 w-4" />
					Documentation
				</Button>
			</div>
		</div>
	</div>
</div>