<script lang="ts">
  import { enhance } from '$app/forms';
  import { UserPlus, LogIn, XCircle, Github } from '@lucide/svelte';
  import Button from '$lib/components/ui/Button.svelte';
  
  export let errorMessage = "";
</script>

<form method="post" action="?/login" use:enhance class="space-y-4">
  <div class="form-control">
    <label for="username" class="label">
      <span class="label-text">Username</span>
    </label>
    <input 
      id="username"
      type="text" 
      name="username" 
      placeholder="Enter your username" 
      class="input input-bordered" 
      required
    />
  </div>
  
  <div class="form-control">
    <label for="password" class="label">
      <span class="label-text">Password</span>
    </label>
    <input 
      id="password"
      type="password" 
      name="password" 
      placeholder="Enter your password" 
      class="input input-bordered" 
      required
    />
  </div>
  
  {#if errorMessage}
    <div class="alert alert-error shadow-sm">
      <XCircle class="stroke-current shrink-0 h-6 w-6" />
      <span>{errorMessage}</span>
    </div>
  {/if}
  
  <div class="card-actions justify-between mt-6">
    <Button type="submit" variant="secondary" formAction="?/register">
      <UserPlus class="w-5 h-5 mr-2" />
      Register
    </Button>
    
    <Button type="submit" variant="primary">
      <LogIn class="w-5 h-5 mr-2" />
      Login
    </Button>
  </div>
</form>

<div class="divider">OR</div>

<div class="flex justify-center">
  <Button variant="outline" size="sm">
    <Github class="w-5 h-5 mr-2" />
    GitHub Login
  </Button>
</div>