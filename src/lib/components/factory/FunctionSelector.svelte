<script lang="ts">
  import { goto } from '$app/navigation';
  import Card from '$lib/components/ui/Card.svelte';
  import { ArrowRight } from '@lucide/svelte';
  
  interface ProviderOption {
    id: string;
    name: string;
    description: string;
    icon: string;
  }
  
  const providerOptions: ProviderOption[] = [
    {
      id: 'anthropic',
      name: 'Anthropic (Claude)',
      description: 'Create a function powered by Claude, Anthropic\'s powerful LLM. Supports function calling and advanced prompting.',
      icon: '🧠'
    },
    {
      id: 'perplexity',
      name: 'Perplexity',
      description: 'Create a function using Perplexity\'s API for search-augmented generation and reasoning.',
      icon: '🔍'
    },
    {
      id: 'ollama',
      name: 'Ollama',
      description: 'Create a function using Ollama to run open source models locally or on your own server.',
      icon: '🦙'
    },
    {
      id: 'database_query',
      name: 'Database Query',
      description: 'Create a function that executes SQL queries against a database with parameterized input.',
      icon: '📊'
    },
    {
      id: 'python_code',
      name: 'Python Code',
      description: 'Create a function that executes custom Python code with the given inputs.',
      icon: '🐍'
    }
  ];
  
  function selectProvider(id: string) {
    if (id === 'anthropic') {
      goto('/factory/new/anthropic');
    } else {
      // For now only Anthropic is implemented
      alert(`Support for ${id} is coming soon!`);
    }
  }
</script>

<div class="space-y-6">
  <Card title="Select Function Type">
    <div class="space-y-4">
      <p class="text-sm opacity-75">
        Choose a function type to create. Each type has specific configuration options and capabilities.
      </p>
      
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {#each providerOptions as option}
          <div 
            class="card bg-base-200 shadow-sm hover:shadow-md transition-all cursor-pointer h-full"
            onclick={() => selectProvider(option.id)}
            onkeydown={(e) => e.key === 'Enter' && selectProvider(option.id)}
            role="button"
            tabindex="0"
          >
            <div class="card-body">
              <div class="text-3xl mb-2">{option.icon}</div>
              <h3 class="card-title text-lg">{option.name}</h3>
              <p class="text-sm opacity-75">{option.description}</p>
              <div class="card-actions justify-end mt-4">
                <button class="btn btn-sm btn-primary">
                  Select
                  <ArrowRight class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </Card>
</div>