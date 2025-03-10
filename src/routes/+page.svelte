<script lang="ts">
  import Button from '$lib/components/ui/Button.svelte';
</script>

<div class="hero min-h-[calc(100vh-64px-56px)] bg-base-200">
  <div class="hero-content text-center">
    <div class="max-w-md">
      <h1 class="text-5xl font-bold">AI Factory</h1>
      <p class="py-6">Your unified platform for AI-powered workflows and data collection. Build, deploy, and scale with ease.</p>
      <div class="flex flex-col sm:flex-row gap-2 justify-center">
        <Button href="/demo" variant="primary">Explore Demos</Button>
        <Button href="https://svelte.dev/docs/kit" variant="outline">Documentation</Button>
      </div>
    </div>
  </div>
</div>
