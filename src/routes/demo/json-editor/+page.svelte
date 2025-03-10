<script lang="ts">
	import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import { onMount } from 'svelte';

	let jsonValue = JSON.stringify(
		{
			name: 'JSON Editor Demo',
			description: 'A simple JSON editor using CodeMirror 6',
			features: ['Syntax highlighting', 'Auto-indentation', 'Error detection', 'Folding'],
			config: {
				enabled: true,
				theme: 'default',
				readOnly: false
			}
		},
		null,
		2
	);

	// Initialize with formatted value from the start
	let formattedValue = jsonValue;

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
		try {
			const parsed = JSON.parse(jsonValue);
			jsonValue = JSON.stringify(parsed, null, 2);
		} catch (error: unknown) {
			const e = error as Error;
			alert('Invalid JSON: ' + e.message);
		}
	}
</script>

<div class="container mx-auto p-4">
	<h1 class="mb-4 text-2xl font-bold">JSON Editor Demo</h1>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
		<Card title="JSON Editor">
			<div class="mb-4 flex items-center justify-between">
				<button class="btn btn-sm" on:click={formatJson}>Format</button>
			</div>

			<JsonEditor
				value={jsonValue}
				onChange={(val) => {
					jsonValue = val;
					handleChange(val);
				}}
				height="400px"
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
		<Card title="Usage Instructions">
			<div class="prose">
				<ul>
					<li>The editor on the left provides syntax highlighting for JSON.</li>
					<li>As you type, the editor validates your JSON.</li>
					<li>The panel on the right shows the formatted output or validation errors.</li>
					<li>Click the "Format" button to auto-format your JSON.</li>
					<li>You can fold objects and arrays using the fold markers in the gutter.</li>
				</ul>
			</div>
		</Card>
	</div>
</div>
