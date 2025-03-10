<script lang="ts">
  import { enhance } from '$app/forms';
  import { ArrowLeft, LogOut, User } from '@lucide/svelte';
  import Button from '$lib/components/ui/Button.svelte';
  
  export let user = { username: "", id: "" };
</script>

<div class="flex flex-col sm:flex-row items-center gap-6 my-6">
  <div class="avatar">
    <div class="bg-base-200 rounded-full w-24 p-5">
      <User class="w-full h-full text-primary" />
    </div>
  </div>
  
  <div>
    <h2 class="text-xl font-semibold">Hi, {user.username}!</h2>
    <div class="badge badge-outline mt-2">User ID: {user.id}</div>
  </div>
</div>

<div class="stats shadow mt-6">
  <div class="stat">
    <div class="stat-title">Account Type</div>
    <div class="stat-value text-primary">Standard</div>
    <div class="stat-desc">Basic access permissions</div>
  </div>
  
  <div class="stat">
    <div class="stat-title">Login Status</div>
    <div class="stat-value text-success">Active</div>
    <div class="stat-desc">Session authenticated</div>
  </div>
</div>

<div class="divider"></div>

<div class="card-actions justify-between items-center">
  <Button href="/demo" variant="ghost">
    <ArrowLeft class="w-5 h-5 mr-2" />
    Back to Demo
  </Button>
  
  <form method="post" action="?/logout" use:enhance>
    <Button type="submit" variant="error">
      <LogOut class="w-5 h-5 mr-2" />
      Sign Out
    </Button>
  </form>
</div>