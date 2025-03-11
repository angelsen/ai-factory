<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import AnthropicEditor from '$lib/components/factory/providers/AnthropicEditor.svelte';
  
  // Get the function ID from the route params
  const functionId = $state(parseInt($page.params.id, 10));
  
  // We'll automatically determine the function type
  let implementationType = $state<string | null>(null);
  let loading = $state(true);
  let error = $state('');
  
  onMount(async () => {
    await fetchFunctionType();
  });
  
  async function fetchFunctionType() {
    try {
      loading = true;
      error = '';
      const response = await fetch(`http://localhost:8000/api/admin/functions/${functionId}`);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      implementationType = data.implementation_type;
    } catch (err) {
      console.error('Error fetching function type:', err);
      error = err instanceof Error ? err.message : 'Unknown error fetching function';
    } finally {
      loading = false;
    }
  }
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold">Edit Function</h1>
    <p class="text-sm opacity-75">Modify an existing function configuration</p>
  </div>
  
  {#if loading}
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body">
        <div class="flex justify-center my-8">
          <span class="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    </div>
  {:else if error}
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body">
        <div class="alert alert-error">
          <p>{error}</p>
          <button class="btn btn-sm btn-outline" onclick={() => fetchFunctionType()}>
            Try Again
          </button>
        </div>
      </div>
    </div>
  {:else}
    {#if implementationType === 'anthropic'}
      <AnthropicEditor {functionId} />
    {:else if implementationType}
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <div class="alert alert-warning">
            <p>Editing {implementationType} functions is not yet supported in the UI.</p>
          </div>
        </div>
      </div>
    {:else}
      <div class="card bg-base-100 shadow-sm">
        <div class="card-body">
          <div class="alert alert-error">
            <p>Unknown function type or function not found.</p>
          </div>
        </div>
      </div>
    {/if}
  {/if}
</div>