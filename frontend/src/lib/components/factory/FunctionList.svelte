<script lang="ts">
  import { onMount } from 'svelte';
  import { Pencil, Trash, Eye, Plus } from '@lucide/svelte';
  import Card from '$lib/components/ui/Card.svelte';

  interface FunctionConfig {
    id: number;
    name: string;
    description: string;
    implementation_type: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
  }

  let functions: FunctionConfig[] = $state([]);
  let loading = $state(true);
  let error = $state('');

  onMount(async () => {
    await loadFunctions();
  });

  async function loadFunctions() {
    try {
      loading = true;
      error = '';
      const response = await fetch('http://localhost:8000/api/admin/functions');
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      functions = await response.json();
    } catch (err) {
      console.error('Error loading functions:', err);
      error = err instanceof Error ? err.message : 'Unknown error loading functions';
    } finally {
      loading = false;
    }
  }
</script>

<Card title="AI Functions">
  <div class="mb-4 flex items-center justify-between">
    <div>
      <button class="btn btn-sm btn-primary flex items-center gap-2" onclick={() => window.location.href = '/factory/new'}>
        <Plus class="h-4 w-4" />
        New Function
      </button>
    </div>
    <div>
      <button class="btn btn-sm btn-outline" onclick={() => loadFunctions()}>
        Refresh
      </button>
    </div>
  </div>

  {#if loading}
    <div class="flex justify-center my-8">
      <span class="loading loading-spinner loading-md"></span>
    </div>
  {:else if error}
    <div class="alert alert-error">
      <p>{error}</p>
      <button class="btn btn-sm btn-outline" onclick={() => loadFunctions()}>
        Try Again
      </button>
    </div>
  {:else if functions.length === 0}
    <div class="alert alert-info">
      <p>No functions found. Create your first function!</p>
    </div>
  {:else}
    <div class="overflow-x-auto">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Status</th>
            <th class="w-24">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each functions as func}
            <tr>
              <td>
                <div class="font-medium">{func.name}</div>
                <div class="text-xs opacity-70">{func.description}</div>
              </td>
              <td>
                <span class="badge badge-sm">
                  {func.implementation_type}
                </span>
              </td>
              <td>
                <span class="badge badge-sm {func.is_active ? 'badge-success' : 'badge-error'}">
                  {func.is_active ? 'Active' : 'Inactive'}
                </span>
              </td>
              <td class="flex gap-1">
                <a href={`/factory/${func.id}`} class="btn btn-xs btn-square btn-outline">
                  <Eye class="h-3 w-3" />
                </a>
                <a href={`/factory/${func.id}/edit`} class="btn btn-xs btn-square btn-outline">
                  <Pencil class="h-3 w-3" />
                </a>
                <button class="btn btn-xs btn-square btn-outline btn-error">
                  <Trash class="h-3 w-3" />
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</Card>