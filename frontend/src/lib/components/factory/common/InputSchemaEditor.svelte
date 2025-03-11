<script lang="ts">
  import JsonEditor from '$lib/components/demo/JsonEditor.svelte';
  
  interface Props {
    schema: string;
    setSchema: (value: string) => void;
    isReadOnly?: boolean;
  }

  let { 
    schema, 
    setSchema,
    isReadOnly = false
  }: Props = $props();

  // Reference to JSON editor with proper $state declaration
  let jsonEditor = $state<JsonEditor | undefined>(undefined);

  // Default schema template
  const defaultSchema = {
    type: 'object',
    properties: {
      message_content: {
        type: 'string',
        description: 'The content to process'
      }
    },
    required: ['message_content']
  };

  // Format the JSON in the editor
  function formatJson() {
    if (jsonEditor) {
      jsonEditor.formatJson();
    }
  }

  // Reset to default schema
  function resetToDefault() {
    if (!isReadOnly) {
      setSchema(JSON.stringify(defaultSchema, null, 2));
      setTimeout(() => {
        if (jsonEditor) jsonEditor.formatJson();
      }, 100);
    }
  }
</script>

<div class="form-control">
  <div id="input-schema-container">
    <label class="label flex justify-between" for="input-schema-editor">
      <span class="label-text">Input Schema (JSON)</span>
      <div class="space-x-2">
        <button 
          type="button" 
          class="btn btn-xs" 
          onclick={() => formatJson()}
          disabled={isReadOnly}
        >
          Format
        </button>
        <button 
          type="button" 
          class="btn btn-xs btn-outline" 
          onclick={() => resetToDefault()}
          disabled={isReadOnly}
        >
          Reset
        </button>
      </div>
    </label>
    <JsonEditor
      bind:this={jsonEditor}
      value={schema}
      onChange={(val) => setSchema(val)}
      height="200px"
      lineWrapping={true}
      readOnly={isReadOnly}
    />
    <div class="label">
      <span class="label-text-alt">Define the input parameters your function accepts</span>
    </div>
  </div>
</div>