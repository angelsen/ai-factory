<script lang="ts">
	import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import { onMount } from 'svelte';
	// Editor reference
	let jsonEditor: JsonEditor | undefined = $state();
	let readOnly = $state(false);
	let lineWrapping = $state(true);

	let jsonValue = $state(
		JSON.stringify(
			{
				name: 'JSON Editor Demo',
				description: 'A simple JSON editor using CodeMirror 6',
				features: [
					'Syntax highlighting',
					'Auto-indentation',
					'Error detection',
					'Folding',
					'Default theme'
				],
				config: {
					enabled: true,
					readOnly: false,
					lineWrapping: true
				}
			},
			null,
			2
		)
	);

	// Initialize with formatted value from the start
	let formattedValue = $state('');

	// This reference needs to be updated when jsonValue changes
	$effect(() => {
		// Update formattedValue when jsonValue changes
		handleChange(jsonValue);
	});

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

<div class="container mx-auto pb-4 px-4">
	<div class="mb-4 flex items-center justify-between">
		<h1 class="text-2xl font-bold">JSON Editor Demo</h1>
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
				onChange={(val: string) => {
					jsonValue = val;
					handleChange(val);
				}}
				height="400px"
				{readOnly}
				{lineWrapping}
			/>
		</Card>

		<Card title="Output">
			<div class="mb-4 flex items-center justify-between">
				<div class="h-[28px]"><!-- Spacer to match button height --></div>
			</div>

			<div class="bg-base-200 h-[400px] overflow-auto rounded-lg p-4">
				<pre>{formattedValue || 'Edit JSON to see output...'}</pre>
			</div>
		</Card>
	</div>

	<div class="mt-6">
		<Card title="JSON Editor Features">
			<div class="prose prose-sm max-w-none">
				<p>
					This JSON editor uses CodeMirror's default theme for a clean and consistent editing
					experience.
				</p>

				<h3>Features</h3>
				<ul>
					<li>Syntax highlighting with CodeMirror's default theme</li>
					<li>Auto-indentation and formatting</li>
					<li>Error detection</li>
					<li>Code folding</li>
					<li>Proper readOnly and lineWrapping support (try the buttons above)</li>
				</ul>
			</div>
		</Card>
	</div>
</div>
