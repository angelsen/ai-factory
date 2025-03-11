<script lang="ts">
	import type { ActionData } from './$types';
	import Card from '$lib/components/ui/Card.svelte';
	import LoginForm from '$lib/components/auth/LoginForm.svelte';

	let { form }: { form: ActionData } = $props();
</script>

<div class="flex justify-center items-center min-h-[calc(100vh-64px-56px)] p-4">
	<Card title="Authentication" width="w-full max-w-md" shadow="shadow-sm">
		<div class="tabs tabs-boxed mb-6">
			<button class="tab tab-active">Login</button>
			<button class="tab">Register</button>
		</div>
		
		<LoginForm errorMessage={form?.message || ""} />
		
		<a href="/demo" class="link link-hover text-center text-sm mt-4 block">Back to demos</a>
	</Card>
</div>
