<script lang="ts">
  export let title = "";
  export let size = "md"; // xs, sm, md, lg, xl
  export let bordered = false;
  export let dashed = false;
  export let imageFull = false;
  export let sideBySide = false;
  export let bgColor = "bg-base-100";
  export let shadow = "shadow-sm";
  export let width = "w-full";
  export let classes = "";
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
  
  {#if $$slots.image}
    <figure>
      <slot name="image"></slot>
    </figure>
  {/if}
  
  <div class="card-body">
    {#if title}
      <h2 class="card-title">{title}</h2>
    {/if}
    
    <slot></slot>
    
    {#if $$slots.actions}
      <div class="card-actions justify-end">
        <slot name="actions"></slot>
      </div>
    {/if}
  </div>
</div>