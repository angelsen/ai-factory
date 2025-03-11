<script lang="ts">
    import { Sparkles } from '@lucide/svelte';

    // Current year
    const currentYear = new Date().getFullYear();
</script>

<footer class="footer footer-center bg-base-200 text-base-content p-6 rounded-t-lg h-16 min-h-[4rem] flex items-center justify-between">
    <div class="flex items-center gap-4">
        <Sparkles 
            class="h-6 w-6 text-secondary opacity-70 hover:opacity-100 transition-opacity" 
        />
        <p class="text-sm">
            © {currentYear} AI Factory. All rights reserved.
        </p>
    </div>
    <div class="flex gap-4">
        <a href="/terms" class="text-xs hover:underline">Terms</a>
        <a href="/privacy" class="text-xs hover:underline">Privacy</a>
        <a href="/contact" class="text-xs hover:underline">Contact</a>
    </div>
</footer>