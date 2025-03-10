<script lang="ts">
  import Card from '$lib/components/ui/Card.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  
  interface Props {
    title?: string;
    description?: string;
    imageUrl?: string;
    badgeLabels?: string[];
    buttonText?: string;
    buttonVariant?: string;
    buttonHref?: string;
    sideBySide?: boolean;
    primaryCard?: boolean;
  }

  let {
    title = "",
    description = "",
    imageUrl = "",
    badgeLabels = [],
    buttonText = "",
    buttonVariant = "primary",
    buttonHref = "",
    sideBySide = false,
    primaryCard = false
  }: Props = $props();
</script>

<Card 
  title={title}
  sideBySide={sideBySide}
  bgColor={primaryCard ? "bg-primary text-primary-content" : "bg-base-100"}
  shadow="shadow-sm"
>
  {#snippet image()}
    <img src={imageUrl} alt={title}  class={!imageUrl ? "hidden" : ""} />
  {/snippet}
  
  <p>{description}</p>
  
  {#if badgeLabels.length > 0}
    <div class="card-actions justify-between mt-4">
      {#each badgeLabels as label}
        <div class="badge badge-outline">{label}</div>
      {/each}
    </div>
  {/if}
  
  {#snippet actions()}
    <div  class={!buttonText ? "hidden" : ""}>
      <Button 
        variant={buttonVariant} 
        href={buttonHref || ""}
      >
        {buttonText}
      </Button>
    </div>
  {/snippet}
</Card>