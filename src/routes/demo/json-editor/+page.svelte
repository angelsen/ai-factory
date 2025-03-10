<script lang="ts">
	import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import { onMount } from 'svelte';
	import ThemeController from '$lib/components/ui/ThemeController.svelte';

	// Editor reference
	let jsonEditor: JsonEditor = $state();
	let readOnly = $state(false);
	let lineWrapping = $state(true);

	let jsonValue = $state(JSON.stringify(
		{
			name: 'JSON Editor Demo',
			description: 'A simple JSON editor using CodeMirror 6',
			features: [
				'Syntax highlighting',
				'Auto-indentation',
				'Error detection',
				'Folding',
				'Theme integration'
			],
			config: {
				enabled: true,
				readOnly: false,
				lineWrapping: true,
				themeSynchronization: true
			},
			themeIntegration: {
				lightTheme: 'Uses DaisyUI light variables',
				darkTheme: 'Automatically switches to dark theme',
				customization: 'Uses semantic colors from current theme'
			}
		},
		null,
		2
	));

	// Initialize with formatted value from the start
	let formattedValue = $state(jsonValue);

	onMount(() => {
		// Process initial value
		handleChange(jsonValue);
	});

	function handleChange(newValue: string): void {
		try {
			// Try to parse and reformat
			const parsed = JSON.parse(newValue);
			formattedValue = JSON.stringify(parsed, null, 2);
		} catch (error: unknown) {
			const e = error as Error;
			formattedValue = e.message;
		}
	}

	function formatJson(): void {
		if (jsonEditor) {
			jsonEditor.formatJson();
		}
	}

	function toggleReadOnly(): void {
		readOnly = !readOnly;
	}

	function toggleLineWrapping(): void {
		lineWrapping = !lineWrapping;
	}
</script>

<div class="container mx-auto p-4">
	<div class="mb-4 flex items-center justify-between">
		<h1 class="text-2xl font-bold">JSON Editor Demo</h1>
		<div class="flex items-center gap-2">
			<span class="text-sm opacity-80">Try different themes:</span>
			<ThemeController />
		</div>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
		<Card title="JSON Editor">
			<div class="mb-4 flex flex-wrap items-center justify-between gap-2">
				<div class="flex flex-wrap gap-2">
					<button class="btn btn-sm btn-primary" onclick={formatJson}>Format</button>
					<button
						class="btn btn-sm {readOnly ? 'btn-error' : 'btn-secondary'}"
						onclick={toggleReadOnly}
					>
						{readOnly ? 'Editable' : 'Read-only'}
					</button>
					<button
						class="btn btn-sm {lineWrapping ? 'btn-success' : 'btn-secondary'}"
						onclick={toggleLineWrapping}
					>
						{lineWrapping ? 'Wrapped' : 'No Wrap'}
					</button>
				</div>
			</div>

			<JsonEditor
				bind:this={jsonEditor}
				value={jsonValue}
				onChange={(val) => {
					jsonValue = val;
					handleChange(val);
				}}
				height="400px"
				{readOnly}
				{lineWrapping}
			/>
		</Card>

		<Card title="Output">
			<div class="h-[400px] overflow-auto rounded-lg bg-base-200 p-4">
				<pre>{formattedValue || 'Edit JSON to see output...'}</pre>
			</div>
		</Card>
	</div>

	<div class="mt-6">
		<Card title="Theme Integration">
			<div class="prose">
				<p>
					This JSON editor automatically adapts to your selected theme! Try changing the theme using
					the selector in the top right corner.
				</p>

				<h3>Features</h3>
				<ul>
					<li>DaisyUI theme integration - automatically uses your current theme's colors</li>
					<li>Smooth transitions between themes</li>
					<li>Semantic syntax highlighting (properties, strings, numbers use appropriate theme colors)</li>
					<li>Support for both light and dark themes</li>
					<li>Real-time theme switching without page reload</li>
					<li>Proper readOnly and lineWrapping support (try the buttons above)</li>
				</ul>
			</div>
		</Card>
	</div>
</div>
