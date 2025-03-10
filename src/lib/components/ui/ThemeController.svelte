<script lang="ts">
	import { onMount } from 'svelte';
	import { Sun, Moon, Monitor, Palette } from '@lucide/svelte';
	import type { ComponentType, SvelteComponent } from 'svelte';

	export let position = 'end'; // start, center, end
	export let size = 'sm'; // sm, md, lg
	export let menuType = 'dropdown'; // dropdown, toggle
	export let additionalThemes = ['synthwave', 'cupcake']; // Additional themes beyond light/dark

	let currentTheme = '';
	const baseThemes = ['light', 'dark', 'system'];
	const allThemes = [...baseThemes, ...additionalThemes];

	// Properly type the themeIcons with index signature for Lucide icons
	type ThemeIconMap = Record<string, any>; // Using any to accommodate Lucide icon components

	const themeIcons: ThemeIconMap = {
		light: Sun,
		dark: Moon,
		system: Monitor,
		// Default icon for additional themes
		...Object.fromEntries(additionalThemes.map((theme) => [theme, Palette]))
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
			on:change={(e) => applyTheme(e.currentTarget.checked ? 'dark' : 'light')}
		/>
		<Sun class="swap-off h-5 w-5 fill-current" />
		<Moon class="swap-on h-5 w-5 fill-current" />
	</label>
{:else}
	<!-- Dropdown theme selector using daisyUI's pattern but with proper ARIA roles -->
	<div class="dropdown dropdown-{position}">
		<div
			tabindex="0"
			role="button"
			aria-haspopup="menu"
			class="btn btn-ghost btn-{size} btn-circle"
		>
			<svelte:component this={themeIcons[currentTheme] || themeIcons.system} class="h-5 w-5" />
		</div>

		<div class="dropdown-content bg-base-100 rounded-box z-[1] shadow">
			<ul role="menu" class="menu p-2">
				{#each allThemes as theme}
					<li role="none">
						<button
							role="menuitem"
							class={currentTheme === theme ? 'active' : ''}
							on:click={() => applyTheme(theme)}
						>
							<svelte:component
								this={themeIcons[theme] || themeIcons.system}
								class="mr-2 h-4 w-4"
							/>
							<span class="capitalize">{theme}</span>
						</button>
					</li>
				{/each}
			</ul>
		</div>
	</div>
{/if}
