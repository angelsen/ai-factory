<script lang="ts">
  import { onMount } from 'svelte';
  import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
  import Card from '$lib/components/ui/Card.svelte';
  import { goto } from '$app/navigation';
  
  // Import common components
  import FunctionHeader from '../common/FunctionHeader.svelte';
  import InputSchemaEditor from '../common/InputSchemaEditor.svelte';
  import FunctionActions from '../common/FunctionActions.svelte';

  interface Props {
    functionId?: number;
    isNew?: boolean;
    isReadOnly?: boolean;
  }

  let { 
    functionId = undefined, 
    isNew = false,
    isReadOnly = false 
  }: Props = $props();
  
  // State
  let name = $state('');
  let description = $state('');
  let isActive = $state(true);
  let inputSchema = $state(JSON.stringify({
    type: 'object',
    properties: {
      message_content: {
        type: 'string',
        description: 'The content to process'
      },
      api_key: {
        type: 'string',
        description: 'Anthropic API key (optional)'
      }
    },
    required: ['message_content']
  }, null, 2));
  
  // Anthropic-specific configuration
  let model = $state('claude-3-opus-20240229');
  let systemPrompt = $state('You are a helpful assistant.');
  let maxTokens = $state(1000);
  let useTools = $state(false);
  let promptTemplate = $state('{message_content}');
  let tools = $state('[]');
  
  // UI state
  let loading = $state(false);
  let saving = $state(false);
  let error = $state('');
  let successMessage = $state('');

  // JSON editor reference
  let toolsEditor = $state<JsonEditor | undefined>(undefined);
  
  // Available Claude models
  const modelOptions = [
    { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
    { value: 'claude-3-sonnet-20240229', label: 'Claude 3 Sonnet' },
    { value: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku' },
    { value: 'claude-3-5-sonnet-20240620', label: 'Claude 3.5 Sonnet' }
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
      
      // Verify this is an Anthropic function
      if (data.implementation_type !== 'anthropic') {
        throw new Error(`Function is not an Anthropic type (type: ${data.implementation_type})`);
      }
      
      // Set basic fields
      name = data.name;
      description = data.description;
      isActive = data.is_active;
      inputSchema = JSON.stringify(data.input_schema, null, 2);
      
      // Set Anthropic-specific fields from implementation_config
      const config = data.implementation_config;
      model = config.model || 'claude-3-opus-20240229';
      systemPrompt = config.system_prompt || '';
      maxTokens = config.max_tokens || 1000;
      promptTemplate = config.prompt_template || '{message_content}';
      
      // Handle tools if present
      if (config.tools && config.tools.length > 0) {
        useTools = true;
        tools = JSON.stringify(config.tools, null, 2);
      } else {
        useTools = false;
        tools = '[]';
      }
      
    } catch (err) {
      console.error('Error loading function:', err);
      error = err instanceof Error ? err.message : 'Unknown error loading function';
    } finally {
      loading = false;
    }
  }

  function formatTools() {
    if (toolsEditor) {
      toolsEditor.formatJson();
    }
  }

  async function saveFunction() {
    try {
      // Validate JSON inputs
      JSON.parse(inputSchema);
      if (useTools) {
        JSON.parse(tools);
      }
      
      saving = true;
      error = '';
      successMessage = '';
      
      // Build Anthropic implementation config
      const implementationConfig = {
        model,
        system_prompt: systemPrompt,
        max_tokens: maxTokens,
        prompt_template: promptTemplate,
        tools: useTools ? JSON.parse(tools) : undefined
      };
      
      // Create form data
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      formData.append('input_schema', inputSchema);
      formData.append('implementation_type', 'anthropic');
      formData.append('implementation_config', JSON.stringify(implementationConfig));
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

  function handleCancel() {
    goto('/factory');
  }

  // Default tools template
  const defaultTools = [
    {
      name: "example_tool",
      description: "An example tool that does something useful",
      input_schema: {
        type: "object",
        properties: {
          param1: {
            type: "string",
            description: "First parameter"
          },
          param2: {
            type: "number",
            description: "Second parameter"
          }
        },
        required: ["param1"]
      }
    }
  ];

  function resetToolsToDefault() {
    tools = JSON.stringify(defaultTools, null, 2);
    setTimeout(() => {
      if (toolsEditor) toolsEditor.formatJson();
    }, 100);
  }
</script>

<div class="space-y-6">
  <Card title={isReadOnly ? "Function Details" : (isNew ? "Create Anthropic Function" : "Edit Anthropic Function")}>
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
        
        <!-- Function header (name, description, active) -->
        <FunctionHeader
          {name}
          setName={(val) => name = val}
          {description}
          setDescription={(val) => description = val}
          {isActive}
          setIsActive={(val) => isActive = val}
          {isNew}
          {isReadOnly}
        />
        
        <!-- Input schema editor -->
        <InputSchemaEditor
          schema={inputSchema}
          setSchema={(val) => inputSchema = val}
          isReadOnly={isReadOnly}
        />
        
        <!-- Anthropic-specific settings -->
        <div class="space-y-4">
          <h3 class="text-lg font-medium">Anthropic Configuration</h3>
          
          <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
            <!-- Model Selection -->
            <div class="form-control">
              <label class="label" for="model-select">
                <span class="label-text">Claude Model</span>
              </label>
              <select 
                id="model-select" 
                class="select select-bordered" 
                value={model}
                onchange={(e) => model = e.currentTarget.value}
                disabled={isReadOnly}
              >
                {#each modelOptions as option}
                  <option value={option.value}>{option.label}</option>
                {/each}
              </select>
            </div>
            
            <!-- Max Tokens -->
            <div class="form-control">
              <label class="label" for="max-tokens">
                <span class="label-text">Max Tokens</span>
              </label>
              <input 
                id="max-tokens"
                type="number" 
                class="input input-bordered" 
                value={maxTokens}
                onchange={(e) => maxTokens = parseInt(e.currentTarget.value, 10)}
                min="1"
                max="100000"
                disabled={isReadOnly}
              />
            </div>
          </div>
          
          <!-- System Prompt -->
          <div class="form-control">
            <label class="label" for="system-prompt">
              <span class="label-text">System Prompt</span>
            </label>
            <textarea 
              id="system-prompt"
              class="textarea textarea-bordered min-h-32" 
              value={systemPrompt}
              onchange={(e) => systemPrompt = e.currentTarget.value}
              placeholder="You are a helpful assistant specialized in..."
              disabled={isReadOnly}
            ></textarea>
          </div>
          
          <!-- Prompt Template -->
          <div class="form-control">
            <label class="label" for="prompt-template">
              <span class="label-text">Prompt Template</span>
            </label>
            <textarea 
              id="prompt-template"
              class="textarea textarea-bordered min-h-24" 
              value={promptTemplate}
              onchange={(e) => promptTemplate = e.currentTarget.value}
              placeholder="Example prompt template with variables"
              disabled={isReadOnly}
            ></textarea>
            <div class="label">
              <span class="label-text-alt">Use {"{variable_name}"} placeholders from the input schema</span>
            </div>
          </div>
          
          <!-- Tools toggle -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-2" for="use-tools">
              <input 
                id="use-tools" 
                type="checkbox" 
                class="toggle toggle-primary" 
                checked={useTools}
                onchange={(e) => useTools = e.currentTarget.checked}
                disabled={isReadOnly}
              />
              <span class="label-text">Use Claude Tools (Function Calling)</span>
            </label>
          </div>
          
          <!-- Tools JSON -->
          {#if useTools}
            <div class="form-control">
              <div id="tools-container">
                <label class="label flex justify-between" for="tools-editor">
                  <span class="label-text">Tools Definition (JSON)</span>
                  <div class="space-x-2">
                    <button 
                      type="button" 
                      class="btn btn-xs" 
                      onclick={() => formatTools()}
                      disabled={isReadOnly}
                    >
                      Format
                    </button>
                    <button 
                      type="button" 
                      class="btn btn-xs btn-outline" 
                      onclick={() => resetToolsToDefault()}
                      disabled={isReadOnly}
                    >
                      Template
                    </button>
                  </div>
                </label>
                <JsonEditor
                  bind:this={toolsEditor}
                  value={tools}
                  onChange={(val) => tools = val}
                  height="200px"
                  lineWrapping={true}
                  readOnly={isReadOnly}
                />
                <div class="label">
                  <span class="label-text-alt">Define the tools that Claude can use for function calling</span>
                </div>
              </div>
            </div>
          {/if}
        </div>
        
        <!-- Action buttons -->
        <FunctionActions
          onSave={saveFunction}
          onCancel={handleCancel}
          saving={saving}
          isReadOnly={isReadOnly}
        />
      </form>
    {/if}
  </Card>
</div>