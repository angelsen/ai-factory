<script lang="ts">
  interface Props {
    title?: string;
    size?: string; // xs, sm, md, lg, xl
    bordered?: boolean;
    dashed?: boolean;
    imageFull?: boolean;
    sideBySide?: boolean;
    bgColor?: string;
    shadow?: string;
    width?: string;
    classes?: string;
    image?: import('svelte').Snippet;
    children?: import('svelte').Snippet;
    actions?: import('svelte').Snippet;
  }

  let {
    title = "",
    size = "md",
    bordered = false,
    dashed = false,
    imageFull = false,
    sideBySide = false,
    bgColor = "bg-base-100",
    shadow = "shadow-sm",
    width = "w-full",
    classes = "",
    image,
    children,
    actions
  }: Props = $props();
</script>

<div class="card {bgColor} {shadow} {width} {classes} 
  {size === 'xs' ? 'card-xs' : ''} 
  {size === 'sm' ? 'card-sm' : ''} 
  {size === 'md' ? 'card-md' : ''} 
  {size === 'lg' ? 'card-lg' : ''} 
  {size === 'xl' ? 'card-xl' : ''} 
  {bordered ? 'card-border' : ''} 
  {dashed ? 'card-dash' : ''} 
  {imageFull ? 'image-full' : ''} 
  {sideBySide ? 'card-side' : ''}">
  
  {#if image}
    <figure>
      {@render image?.()}
    </figure>
  {/if}
  
  <div class="card-body">
    {#if title}
      <h2 class="card-title">{title}</h2>
    {/if}
    
    {@render children?.()}
    
    {#if actions}
      <div class="card-actions justify-end">
        {@render actions?.()}
      </div>
    {/if}
  </div>
</div>