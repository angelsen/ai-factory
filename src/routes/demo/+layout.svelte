<script lang="ts">
    import { page } from '$app/stores';
    
    // Props to access the children
    let { children } = $props();
    
    // Track the current route to determine if content should be scrollable
    $effect(() => {
        // Optional: You can use this to selectively apply the scrollable layout to specific routes
        // For now we'll apply it to all routes under /demo/
        isScrollableRoute = $page.url.pathname.startsWith('/demo/');
    });
    
    // State to determine if the content should be scrollable
    let isScrollableRoute = $state(true);
</script>

{#if isScrollableRoute}
    <!-- Scrollable layout for demo pages -->
    <div class="scrollable-content-wrapper flex-grow overflow-hidden flex flex-col">
        <div class="scrollable-content h-full overflow-y-auto">
            {@render children()}
        </div>
    </div>
{:else}
    <!-- Regular layout for other pages -->
    <div class="flex-grow">
        {@render children()}
    </div>
{/if}

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