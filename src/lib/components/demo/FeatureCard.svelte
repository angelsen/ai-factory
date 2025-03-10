<script lang="ts">
  import Card from '$lib/components/ui/Card.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  
  export let title = "";
  export let description = "";
  export let imageUrl = "";
  export let badgeLabels: string[] = [];
  export let buttonText = "";
  export let buttonVariant = "primary";
  export let buttonHref = "";
  export let sideBySide = false;
  export let primaryCard = false;
</script>

<Card 
  title={title}
  sideBySide={sideBySide}
  bgColor={primaryCard ? "bg-primary text-primary-content" : "bg-base-100"}
  shadow="shadow-sm"
>
  <img src={imageUrl} alt={title} slot="image" class={!imageUrl ? "hidden" : ""} />
  
  <p>{description}</p>
  
  {#if badgeLabels.length > 0}
    <div class="card-actions justify-between mt-4">
      {#each badgeLabels as label}
        <div class="badge badge-outline">{label}</div>
      {/each}
    </div>
  {/if}
  
  <div slot="actions" class={!buttonText ? "hidden" : ""}>
    <Button 
      variant={buttonVariant} 
      href={buttonHref || ""}
    >
      {buttonText}
    </Button>
  </div>
</Card>