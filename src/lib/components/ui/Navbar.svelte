<script lang="ts">
	import { Menu, Github, Sparkles } from '@lucide/svelte';
	import ThemeController from './ThemeController.svelte';

	interface Props {
		logo?: string;
		githubUrl?: string;
		showThemeController?: boolean;
	}

	let {
		logo = 'AI Factory',
		githubUrl = 'https://github.com/angelsen/ai-factory',
		showThemeController = true
	}: Props = $props();
</script>

<div class="navbar bg-base-100 shadow-sm h-16 min-h-[4rem]">
	<div class="navbar-start">
		<div class="dropdown">
			<button class="btn btn-ghost lg:hidden">
				<Menu class="h-5 w-5" />
			</button>
			<div class="dropdown-content menu menu-sm bg-base-100 rounded-box z-[100] mt-3 p-2 shadow">
				<li><a href="/">Home</a></li>
				<li><a href="/factory">AI Factory</a></li>
				<li><a href="/demo">Demo</a></li>
				<li>
					<a href="#auth-dropdown" aria-haspopup="true">Authentication</a>
					<ul class="p-2" id="auth-dropdown">
						<li><a href="/demo/lucia">Lucia Auth</a></li>
						<li><a href="/demo/lucia/login">Login</a></li>
					</ul>
				</li>
			</div>
		</div>
		<div class="navbar-start flex items-center lg:justify-start justify-center">
			<div class="relative group">
				<a 
					href="/" 
					class="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-xl font-medium relative z-10 group-hover:scale-105 transition-all duration-300 bg-transparent group-hover:text-accent"
				>
					<span>AI Factory</span>
					<div class="relative">
						<Sparkles 
							class="h-5 w-5 text-secondary group-hover:text-accent transition-colors duration-300" 
							strokeWidth={1.5} 
						/>
						<div class="absolute inset-0 rounded-full blur-lg bg-secondary/60 -z-10 scale-[2] group-hover:bg-accent/70 group-hover:scale-[2.5] transition-all duration-300"></div>
					</div>
				</a>
				<!-- Glow effect container -->
				<div class="absolute inset-0 bg-gradient-to-r from-primary/30 via-secondary/40 to-accent/30 blur-xl opacity-0 group-hover:opacity-100 rounded-lg transition-all duration-500 -z-10 scale-110 group-hover:scale-125"></div>
			</div>
		</div>
	</div>
	<div class="navbar-center hidden lg:flex">
		<ul class="menu menu-horizontal px-1">
			<li><a href="/">Home</a></li>
			<li><a href="/factory">AI Factory</a></li>
			<li><a href="/demo">Demo</a></li>
			<li>
				<details>
					<summary>Authentication</summary>
					<ul class="bg-base-100 z-[100] p-2">
						<li><a href="/demo/lucia">Lucia Auth</a></li>
						<li><a href="/demo/lucia/login">Login</a></li>
					</ul>
				</details>
			</li>
		</ul>
	</div>
	<div class="navbar-end gap-2">
		{#if showThemeController}
			<ThemeController position="left" size="sm" />
		{/if}
		<a href={githubUrl} class="btn btn-ghost btn-circle">
			<Github />
		</a>
	</div>
</div>