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

<div class="space-y-4">
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
    <!-- Function Name -->
    <div class="form-control">
      <label class="label" for="function-name">
        <span class="label-text">Function Name</span>
      </label>
      <input 
        id="function-name"
        type="text" 
        class="input input-bordered" 
        value={name}
        onchange={(e) => setName(e.currentTarget.value)}
        required 
        placeholder="generate_wiki"
        readonly={isReadOnly}
      />
    </div>
    
    <!-- Active Toggle -->
    <div class="form-control">
      <div class="h-10"></div> <!-- Spacer to align with other field -->
      <label class="label cursor-pointer justify-start gap-2" for="function-active">
        <input 
          id="function-active" 
          type="checkbox" 
          class="toggle toggle-success" 
          checked={isActive}
          onchange={(e) => setIsActive(e.currentTarget.checked)} 
          disabled={isReadOnly}
        />
        <span class="label-text">Active</span>
      </label>
    </div>
  </div>
  
  <!-- Description -->
  <div class="form-control">
    <label class="label" for="description">
      <span class="label-text">Description</span>
    </label>
    <textarea 
      id="description"
      class="textarea textarea-bordered min-h-24" 
      value={description}
      onchange={(e) => setDescription(e.currentTarget.value)}
      placeholder="What does this function do?"
      readonly={isReadOnly}
    ></textarea>
  </div>
</div>