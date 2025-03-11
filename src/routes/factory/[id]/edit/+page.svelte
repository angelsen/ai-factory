<script lang="ts">
  import { page } from '$app/stores';
  import FunctionEditor from '$lib/components/factory/FunctionEditor.svelte';
  
  // Get the function ID from the route params
  const functionId = $state(parseInt($page.params.id, 10));
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold">Edit Function</h1>
    <p class="text-sm opacity-75">Modify an existing function configuration</p>
  </div>
  
  <FunctionEditor functionId={functionId} />
</div>