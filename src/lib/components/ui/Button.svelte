<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher<{click: MouseEvent}>();
  
  interface Props {
    type?: 'button' | 'submit' | 'reset';
    variant?: string; // primary, secondary, accent, ghost, link, outline, error
    size?: string; // lg, md, sm, xs
    fullWidth?: boolean;
    disabled?: boolean;
    href?: string;
    formAction?: string;
    className?: string; // Custom CSS classes to be added
    children?: import('svelte').Snippet;
  }

  let {
    type = "button",
    variant = "",
    size = "",
    fullWidth = false,
    disabled = false,
    href = "",
    formAction = "",
    className = "",
    children
  }: Props = $props();
  
  function handleClick(event: MouseEvent) {
    dispatch('click', event);
  }
</script>

{#if href}
  <a {href} 
    class="btn {variant ? `btn-${variant}` : ''} {size ? `btn-${size}` : ''} {fullWidth ? 'btn-block' : ''} {className}"
    class:disabled
    onclick={handleClick}>
    {@render children?.()}
  </a>
{:else}
  <button 
    {type} 
    {disabled} 
    formaction={formAction || undefined}
    class="btn {variant ? `btn-${variant}` : ''} {size ? `btn-${size}` : ''} {fullWidth ? 'btn-block' : ''} {className}"
    onclick={handleClick}>
    {@render children?.()}
  </button>
{/if}