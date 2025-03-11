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
					class="btn btn-ghost text-xl relative z-10 group-hover:scale-100 transition-transform duration-300 flex items-center gap-2"
				>
					AI Factory
					<div class="relative">
						<Sparkles 
							class="h-5 w-5 text-secondary" 
							strokeWidth={1.5} 
						/>
						<div class="absolute inset-0 rounded-full blur-md bg-secondary/30 -z-10 scale-150 animate-pulse"></div>
					</div>
				</a>
				<div class="absolute inset-0 bg-secondary/20 blur-md opacity-0 group-hover:opacity-100 rounded-lg transition-all duration-300 -z-10 scale-110 animate-pulse"></div>
			</div>
		</div>
	</div>
	<div class="navbar-center hidden lg:flex">
		<ul class="menu menu-horizontal px-1">
			<li><a href="/">Home</a></li>
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