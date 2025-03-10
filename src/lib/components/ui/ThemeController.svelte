<script lang="ts">
	import { onMount } from 'svelte';
	import { Sun, Moon, Monitor, Palette } from '@lucide/svelte';
	import type { ComponentType, SvelteComponent } from 'svelte';

	interface Props {
		position?: string; // start, center, end
		size?: string; // sm, md, lg
		menuType?: string; // dropdown, toggle
		additionalThemes?: any; // Additional themes beyond light/dark
	}

	// Import theme constants
	import { BASE_THEMES, ADDITIONAL_THEMES } from '$lib/theme';

	let {
		position = 'end',
		size = 'sm',
		menuType = 'dropdown',
		additionalThemes = ADDITIONAL_THEMES
	}: Props = $props();

	let currentTheme = $state('');
	const baseThemes = BASE_THEMES;
	const allThemes = [...baseThemes, ...additionalThemes];

	// Properly type the themeIcons with index signature for Lucide icons
	type ThemeIconMap = Record<string, any>; // Using any to accommodate Lucide icon components

	const themeIcons: ThemeIconMap = {
		light: Sun,
		dark: Moon,
		system: Monitor,
		// Default icon for additional themes
		...Object.fromEntries(additionalThemes.map((theme: string) => [theme, Palette]))
	};

	// Initialize theme on mount
	onMount(() => {
		// Get stored theme or default to system
		currentTheme = localStorage.getItem('theme') || 'system';

		// Set initial theme
		applyTheme(currentTheme);

		// Listen for system preference changes if using system
		if (currentTheme === 'system') {
			const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
			const updateThemeFromSystem = () => {
				document.documentElement.setAttribute(
					'data-theme',
					darkModeMediaQuery.matches ? 'dark' : 'light'
				);
			};

			darkModeMediaQuery.addEventListener('change', updateThemeFromSystem);
			updateThemeFromSystem();

			return () => darkModeMediaQuery.removeEventListener('change', updateThemeFromSystem);
		}
	});

	function applyTheme(theme: string) {
		if (theme === 'system') {
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
		} else {
			document.documentElement.setAttribute('data-theme', theme);
		}
		localStorage.setItem('theme', theme);
		currentTheme = theme;
	}
</script>

{#if menuType === 'toggle'}
	<!-- Sun/Moon toggle switch -->
	<label class="swap swap-rotate {size === 'sm' ? 'swap-sm' : size === 'lg' ? 'swap-lg' : ''}">
		<input
			type="checkbox"
			checked={currentTheme === 'dark'}
			onchange={(e) => applyTheme(e.currentTarget.checked ? 'dark' : 'light')}
		/>
		<Sun class="swap-off h-5 w-5 fill-current" />
		<Moon class="swap-on h-5 w-5 fill-current" />
	</label>
{:else}
	<!-- Dropdown theme selector using daisyUI's pattern with proper ARIA roles -->
	{@const SvelteComponent_1 = themeIcons[currentTheme] || themeIcons.system}
	<div class="dropdown dropdown-left">
		<div
			tabindex="0"
			role="button"
			aria-haspopup="menu"
			class="btn btn-ghost btn-{size} btn-circle m-1"
		>
			<SvelteComponent_1 class="h-5 w-5" />
		</div>

		<ul
			role="menu"
			tabindex="0"
			class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow"
		>
			{#each allThemes as theme}
				{@const SvelteComponent_2 = themeIcons[theme] || themeIcons.system}
				<li role="none">
					<button
						role="menuitem"
						class={currentTheme === theme ? 'active' : ''}
						onclick={() => applyTheme(theme)}
					>
						<SvelteComponent_2 class="mr-2 h-4 w-4" />
						<span class="capitalize">{theme}</span>
					</button>
				</li>
			{/each}
		</ul>
	</div>
{/if}
