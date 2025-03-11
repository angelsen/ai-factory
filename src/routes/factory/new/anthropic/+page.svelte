<script lang="ts">
  import AnthropicEditor from '$lib/components/factory/providers/AnthropicEditor.svelte';
</script>

<div class="container mx-auto pb-8 px-4">
  <div class="mb-6">
    <h1 class="text-2xl font-bold">Create Anthropic Function</h1>
    <p class="text-sm opacity-75">Configure a new function powered by Claude</p>
  </div>
  
  <AnthropicEditor isNew={true} />
</div>