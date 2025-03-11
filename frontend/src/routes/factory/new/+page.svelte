<script lang="ts">
  import FunctionSelector from '$lib/components/factory/FunctionSelector.svelte';
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold">Create New Function</h1>
    <p class="text-sm opacity-75">Select the type of function you want to create</p>
  </div>
  
  <FunctionSelector />
</div>