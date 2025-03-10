<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher<{click: MouseEvent}>();
  
  export let type: 'button' | 'submit' | 'reset' = "button";
  export let variant = ""; // primary, secondary, accent, ghost, link, outline, error
  export let size = ""; // lg, md, sm, xs
  export let fullWidth = false;
  export let disabled = false;
  export let href = "";
  export let formAction = "";
  
  function handleClick(event: MouseEvent) {
    dispatch('click', event);
  }
</script>

{#if href}
  <a {href} 
    class="btn {variant ? `btn-${variant}` : ''} {size ? `btn-${size}` : ''} {fullWidth ? 'btn-block' : ''}"
    class:disabled
    on:click={handleClick}>
    <slot></slot>
  </a>
{:else}
  <button 
    {type} 
    {disabled} 
    formaction={formAction || undefined}
    class="btn {variant ? `btn-${variant}` : ''} {size ? `btn-${size}` : ''} {fullWidth ? 'btn-block' : ''}"
    on:click={handleClick}>
    <slot></slot>
  </button>
{/if}