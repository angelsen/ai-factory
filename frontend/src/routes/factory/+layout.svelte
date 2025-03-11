<script lang="ts">
    import { page } from '$app/stores';
    
    // Props to access the children
    let { children } = $props();
</script>

<!-- Scrollable layout for factory pages -->
<div class="scrollable-content-wrapper flex-grow overflow-hidden flex flex-col">
    <div class="scrollable-content h-full overflow-y-auto pb-24"> <!-- Added bottom padding for footer -->
        {@render children()}
    </div>
</div>

<style>
    /* Make sure the scrollable container takes the full available space */
    .scrollable-content-wrapper {
        height: calc(100vh - 8rem); /* Adjust based on your navbar (4rem) and footer (4rem) heights */
    }
    
    /* Add a subtle scrollbar styling */
    .scrollable-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .scrollable-content::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.05);
        border-radius: 4px;
    }
    
    .scrollable-content::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.15);
        border-radius: 4px;
    }
    
    .scrollable-content::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 0, 0, 0.25);
    }
</style>