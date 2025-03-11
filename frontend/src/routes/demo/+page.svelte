<script lang="ts">
  import FeatureCard from '$lib/components/demo/FeatureCard.svelte';
</script>

<div class="p-6 pb-8">
  <h1 class="text-3xl font-bold mb-6">Demo Components</h1>
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Authentication Card -->
    <FeatureCard
      title="Authentication Demo"
      description="Explore the Lucia authentication implementation with login functionality."
      buttonText="Try Lucia Auth"
      buttonVariant="primary"
      buttonHref="/demo/lucia"
    />

    <!-- JSON Editor Card -->
    <FeatureCard
      title="JSON Editor"
      description="Interactive JSON editor with syntax highlighting, validation, and formatting."
      badgeLabels={["CodeMirror", "JSON", "Svelte"]}
      buttonText="Try JSON Editor"
      buttonVariant="secondary"
      buttonHref="/demo/json-editor"
    />

    <!-- AI Workflow Card -->
    <FeatureCard
      title="AI Workflow"
      description="Automated AI processing pipelines."
      imageUrl="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.webp"
      buttonText="Coming Soon"
      buttonVariant="accent"
      sideBySide={true}
    />

    <!-- Components Card -->
    <FeatureCard
      title="UI Components"
      description="Explore the various daisyUI components used throughout the application."
      badgeLabels={["DaisyUI", "Tailwind CSS", "SvelteKit"]}
      buttonText="Coming Soon"
      buttonVariant="ghost"
    />

    <!-- Dashboard Card -->
    <FeatureCard
      title="Dashboard Demo"
      description="Interactive analytics dashboard with real-time data visualization."
      buttonText="Coming Soon"
      primaryCard={true}
    />

    <!-- API Integration Card -->
    <FeatureCard
      title="API Integration"
      description="Connect with external services and data providers."
      buttonText="Coming Soon"
      buttonVariant="outline"
    />
  </div>
</div>
