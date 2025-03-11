<script lang="ts">
  import FunctionEditor from '$lib/components/factory/FunctionEditor.svelte';
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold">Create New Function</h1>
    <p class="text-sm opacity-75">Define a new AI function configuration</p>
  </div>
  
  <FunctionEditor isNew={true} />
</div>