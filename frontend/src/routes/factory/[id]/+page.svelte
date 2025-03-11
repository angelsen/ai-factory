<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
  import { Edit, Play, ArrowLeft } from '@lucide/svelte';
  import AnthropicEditor from '$lib/components/factory/providers/AnthropicEditor.svelte';
  
  // Get the function ID from the route params
  const functionId = parseInt($page.params.id, 10);
  
  // Define the function data type
  interface FunctionData {
    id: number;
    name: string;
    description: string;
    input_schema: any;
    implementation_type: string;
    implementation_config: any;
    is_active: boolean;
    created_at: string;
    updated_at: string;
  }
  
  // UI state
  let function_data = $state<FunctionData | null>(null);
  let loading = $state(true);
  let error = $state('');
  let showEditor = $state(false);
  
  onMount(async () => {
    await loadFunction();
  });
  
  async function loadFunction() {
    try {
      loading = true;
      error = '';
      const response = await fetch(`http://localhost:8000/api/admin/functions/${functionId}`);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      function_data = await response.json();
    } catch (err) {
      console.error('Error loading function:', err);
      error = err instanceof Error ? err.message : 'Unknown error loading function';
    } finally {
      loading = false;
    }
  }
  
  function toggleView() {
    showEditor = !showEditor;
  }
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6 flex items-center gap-2">
    <a href="/factory" class="btn btn-ghost btn-sm">
      <ArrowLeft class="h-4 w-4" />
      Back to functions
    </a>
  </div>
  
  {#if loading}
    <div class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
  {:else if error}
    <div class="alert alert-error">
      <p>{error}</p>
      <button class="btn btn-sm btn-outline" onclick={() => loadFunction()}>
        Try Again
      </button>
    </div>
  {:else if function_data}
    {#if showEditor && function_data.implementation_type === 'anthropic'}
      <AnthropicEditor functionId={functionId} isReadOnly={true} />
    {:else}
      <div class="space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold">{function_data.name}</h1>
            <p class="text-sm opacity-75">
              {function_data.description}
            </p>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-outline btn-sm gap-2" onclick={toggleView}>
              {showEditor ? 'Simple View' : 'Detailed View'}
            </button>
            <a href={`/factory/${functionId}/edit`} class="btn btn-outline btn-sm gap-2">
              <Edit class="h-4 w-4" />
              Edit
            </a>
            <button class="btn btn-primary btn-sm gap-2">
              <Play class="h-4 w-4" />
              Test
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <!-- Function Info Card -->
          <Card title="Function Information">
            <div class="space-y-4">
              <div>
                <div class="font-semibold">Implementation Type</div>
                <div class="badge badge-lg">
                  {#if function_data.implementation_type === 'anthropic'}
                    Anthropic (Claude)
                  {:else}
                    {function_data.implementation_type}
                  {/if}
                </div>
              </div>
              
              <div>
                <div class="font-semibold">Status</div>
                <div class="badge badge-lg {function_data.is_active ? 'badge-success' : 'badge-error'}">
                  {function_data.is_active ? 'Active' : 'Inactive'}
                </div>
              </div>
              
              <div>
                <div class="font-semibold">Created</div>
                <div>{new Date(function_data.created_at).toLocaleString()}</div>
              </div>
              
              <div>
                <div class="font-semibold">Last Updated</div>
                <div>{new Date(function_data.updated_at).toLocaleString()}</div>
              </div>
              
              <div>
                <div class="font-semibold">API Endpoint</div>
                <div class="bg-base-200 p-2 rounded font-mono text-sm overflow-x-auto">
                  POST http://localhost:8000/api/functions/{function_data.name}
                </div>
              </div>
            </div>
          </Card>
          
          <!-- Input Schema Card -->
          <Card title="Input Schema">
            <div class="h-[300px] bg-base-200 rounded-lg overflow-auto">
              <JsonEditor 
                value={JSON.stringify(function_data.input_schema, null, 2)} 
                readOnly={true}
                lineWrapping={true}
                height="300px"
              />
            </div>
          </Card>
          
          <!-- Implementation Config Card -->
          <Card title="Implementation Configuration" classes="lg:col-span-2">
            <div class="h-[300px] bg-base-200 rounded-lg overflow-auto">
              <JsonEditor 
                value={JSON.stringify(function_data.implementation_config, null, 2)} 
                readOnly={true}
                lineWrapping={true}
                height="300px"
              />
            </div>
          </Card>
        </div>
      </div>
    {/if}
  {/if}
</div>