<script lang="ts">
	import type { PageServerData } from './$types';
	import Card from '$lib/components/ui/Card.svelte';
	import UserProfile from '$lib/components/auth/UserProfile.svelte';

	let { data }: { data: PageServerData } = $props();
</script>

<div class="p-6 max-w-4xl mx-auto">
	<Card title="User Profile" size="md" shadow="shadow-sm">
		<UserProfile user={data.user} />
	</Card>
</div>
