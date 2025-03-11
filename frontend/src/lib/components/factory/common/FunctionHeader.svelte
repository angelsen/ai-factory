<script lang="ts">
  interface Props {
    name: string;
    setName: (value: string) => void;
    description: string;
    setDescription: (value: string) => void;
    isActive: boolean; 
    setIsActive: (value: boolean) => void;
    isNew?: boolean;
    isReadOnly?: boolean;
  }

  let { 
    name, 
    setName, 
    description, 
    setDescription, 
    isActive, 
    setIsActive,
    isNew = false,
    isReadOnly = false
  }: Props = $props();
</script>

<div class="space-y-6">
  <div class="border-b border-base-300 pb-2">
    <h3 class="text-lg font-medium">Basic Information</h3>
  </div>

  <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
    <!-- Function Name -->
    <div class="form-control w-full">
      <label class="label" for="function-name">
        <span class="label-text font-medium">Function Name</span>
      </label>
      <input 
        id="function-name"
        type="text" 
        class="input input-bordered w-full" 
        value={name}
        onchange={(e) => setName(e.currentTarget.value)}
        required 
        placeholder="generate_wiki"
        readonly={isReadOnly}
      />
    </div>
    
    <!-- Active Toggle -->
    <div class="form-control w-full flex items-center">
      <label class="label self-start" for="function-active">
        <span class="label-text font-medium">Status</span>
      </label>
      <div class="flex items-center gap-2 mt-2">
        <input 
          id="function-active" 
          type="checkbox" 
          class="toggle toggle-success" 
          checked={isActive}
          onchange={(e) => setIsActive(e.currentTarget.checked)} 
          disabled={isReadOnly}
        />
        <span class="text-sm">{isActive ? 'Active' : 'Inactive'}</span>
      </div>
    </div>
  </div>
  
  <!-- Description -->
  <div class="form-control w-full">
    <label class="label" for="description">
      <span class="label-text font-medium">Description</span>
    </label>
    <textarea 
      id="description"
      class="textarea textarea-bordered min-h-24 w-full" 
      value={description}
      onchange={(e) => setDescription(e.currentTarget.value)}
      placeholder="What does this function do?"
      readonly={isReadOnly}
    ></textarea>
  </div>
</div>