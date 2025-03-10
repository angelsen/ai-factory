<script lang="ts">
	import { Menu, Github } from '@lucide/svelte';
	import ThemeController from './ThemeController.svelte';

	interface Props {
		logo?: string;
		githubUrl?: string;
		showThemeController?: boolean;
	}

	let { logo = 'AI Factory', githubUrl = 'https://github.com/angelsen/ai-factory', showThemeController = true }: Props = $props();
</script>

<div class="navbar bg-base-100 shadow-sm">
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
		<a href="/" class="btn btn-ghost text-xl">{logo}</a>
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