<script lang="ts">
  import { onMount } from 'svelte';
  import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import { goto } from '$app/navigation';

  interface Props {
    functionId?: number;
    isNew?: boolean;
  }

  let { functionId = undefined, isNew = false }: Props = $props();
  
  let name = $state('');
  let description = $state('');
  let implementationType = $state('anthropic');
  let isActive = $state(true);
  let inputSchema = $state(JSON.stringify({
    type: 'object',
    properties: {
      message_content: {
        type: 'string',
        description: 'The content to process'
      }
    },
    required: ['message_content']
  }, null, 2));
  
  let implementationConfig = $state(JSON.stringify({
    model: 'claude-3-5-sonnet',
    max_tokens: 1000,
    system_prompt: 'You are a helpful assistant.',
    prompt_template: '{message_content}'
  }, null, 2));

  let loading = $state(false);
  let saving = $state(false);
  let error = $state('');
  let successMessage = $state('');

  // Reference to JSON editors with proper $state declaration for Svelte 5
  let inputSchemaEditor = $state<JsonEditor | undefined>(undefined);
  let implementationConfigEditor = $state<JsonEditor | undefined>(undefined);
  
  // Available implementation types
  const implementationTypes = [
    { value: 'anthropic', label: 'Anthropic (Claude)' },
    { value: 'perplexity', label: 'Perplexity' },
    { value: 'ollama', label: 'Ollama' },
    { value: 'database_query', label: 'Database Query' },
    { value: 'python_code', label: 'Python Code' }
  ];

  onMount(async () => {
    if (!isNew && functionId) {
      await loadFunction(functionId);
    }
  });

  async function loadFunction(id: number) {
    try {
      loading = true;
      error = '';
      const response = await fetch(`http://localhost:8000/api/admin/functions/${id}`);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      
      name = data.name;
      description = data.description;
      implementationType = data.implementation_type;
      isActive = data.is_active;
      inputSchema = JSON.stringify(data.input_schema, null, 2);
      implementationConfig = JSON.stringify(data.implementation_config, null, 2);
    } catch (err) {
      console.error('Error loading function:', err);
      error = err instanceof Error ? err.message : 'Unknown error loading function';
    } finally {
      loading = false;
    }
  }

  async function saveFunction() {
    try {
      // Validate JSON
      JSON.parse(inputSchema);
      JSON.parse(implementationConfig);
      
      saving = true;
      error = '';
      successMessage = '';
      
      // Create form data
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      formData.append('input_schema', inputSchema);
      formData.append('implementation_type', implementationType);
      formData.append('implementation_config', implementationConfig);
      formData.append('is_active', isActive.toString());
      
      let url = 'http://localhost:8000/api/admin/functions';
      let method = 'POST';
      
      if (!isNew && functionId) {
        url = `http://localhost:8000/api/admin/functions/${functionId}`;
        method = 'PUT';
      }
      
      const response = await fetch(url, {
        method,
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        successMessage = 'Function saved successfully!';
        
        // If this was a new function, redirect to the edit page
        if (isNew) {
          setTimeout(() => {
            goto(`/factory/${result.function_id}/edit`);
          }, 1000);
        }
      } else {
        throw new Error(result.error || 'Unknown error saving function');
      }
    } catch (err) {
      console.error('Error saving function:', err);
      error = err instanceof Error ? err.message : 'Unknown error saving function';
    } finally {
      saving = false;
    }
  }

  function formatJson() {
    if (inputSchemaEditor) {
      inputSchemaEditor.formatJson();
    }
    if (implementationConfigEditor) {
      implementationConfigEditor.formatJson();
    }
  }
</script>

<div class="space-y-6">
  <Card title={isNew ? "Create New Function" : "Edit Function"}>
    {#if loading}
      <div class="flex justify-center my-8">
        <span class="loading loading-spinner loading-md"></span>
      </div>
    {:else}
      <form onsubmit={(e) => { e.preventDefault(); saveFunction(); }} class="space-y-4">
        {#if error}
          <div class="alert alert-error">
            <p>{error}</p>
          </div>
        {/if}
        
        {#if successMessage}
          <div class="alert alert-success">
            <p>{successMessage}</p>
          </div>
        {/if}
        
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div class="form-control">
            <label class="label" for="function-name">
              <span class="label-text">Function Name</span>
            </label>
            <input 
              id="function-name"
              type="text" 
              class="input input-bordered" 
              bind:value={name} 
              required 
              placeholder="generate_wiki"
            />
          </div>
          
          <div class="form-control">
            <label class="label" for="implementation-type">
              <span class="label-text">Implementation Type</span>
            </label>
            <select id="implementation-type" class="select select-bordered" bind:value={implementationType}>
              {#each implementationTypes as type}
                <option value={type.value}>{type.label}</option>
              {/each}
            </select>
          </div>
        </div>
        
        <div class="form-control">
          <label class="label" for="description">
            <span class="label-text">Description</span>
          </label>
          <textarea 
            id="description"
            class="textarea textarea-bordered min-h-24" 
            bind:value={description} 
            placeholder="What does this function do?"
          ></textarea>
        </div>
        
        <div class="form-control">
          <div id="input-schema-container">
            <label class="label flex justify-between" for="input-schema-editor">
              <span class="label-text">Input Schema (JSON)</span>
              <button type="button" class="btn btn-xs" onclick={() => formatJson()}>Format JSON</button>
            </label>
            <JsonEditor
              bind:this={inputSchemaEditor}
              value={inputSchema}
              onChange={(val) => inputSchema = val}
              height="200px"
              lineWrapping={true}
            />
            <div class="label">
              <span class="label-text-alt">Define the input parameters your function accepts</span>
            </div>
          </div>
        </div>
        
        <div class="form-control">
          <div id="implementation-config-container">
            <label class="label" for="implementation-config-editor">
              <span class="label-text">Implementation Config (JSON)</span>
            </label>
            <JsonEditor
              bind:this={implementationConfigEditor}
              value={implementationConfig}
              onChange={(val) => implementationConfig = val}
              height="300px"
              lineWrapping={true}
            />
            <div class="label">
              <span class="label-text-alt">Configuration specific to the implementation type</span>
            </div>
          </div>
        </div>
        
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-2" for="function-active">
            <input id="function-active" type="checkbox" class="toggle toggle-success" bind:checked={isActive} />
            <span class="label-text">Active</span>
          </label>
        </div>
        
        <div class="flex justify-between mt-6">
          <a href="/factory" class="btn btn-outline">Cancel</a>
          <button type="submit" class="btn btn-primary" disabled={saving}>
            {#if saving}
              <span class="loading loading-spinner loading-xs"></span>
              Saving...
            {:else}
              Save Function
            {/if}
          </button>
        </div>
      </form>
    {/if}
  </Card>
</div>