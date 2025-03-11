<script lang="ts">
  interface Props {
    onSave: () => Promise<void>;
    onCancel: () => void;
    saving?: boolean;
    isReadOnly?: boolean;
  }

  let { 
    onSave, 
    onCancel, 
    saving = false,
    isReadOnly = false 
  }: Props = $props();
</script>

<div class="flex justify-between mt-8 pt-4 border-t border-base-300">
  <button 
    type="button" 
    class="btn btn-outline" 
    onclick={onCancel}
  >
    {isReadOnly ? 'Back' : 'Cancel'}
  </button>
  
  {#if !isReadOnly}
    <button 
      type="submit" 
      class="btn btn-primary min-w-[150px]" 
      disabled={saving}
      onclick={() => onSave()}
    >
      {#if saving}
        <span class="loading loading-spinner loading-xs mr-2"></span>
        Saving...
      {:else}
        Save Function
      {/if}
    </button>
  {/if}
</div>