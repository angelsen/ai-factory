<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, basicSetup } from 'codemirror';
  import { EditorState } from '@codemirror/state';
  import { json } from '@codemirror/lang-json';

  interface Props {
    value?: string;
    onChange?: (val: string) => void;
    height?: string;
    readOnly?: boolean;
    lineWrapping?: boolean;
    language?: string;
  }

  let {
    value = '',
    onChange = (val: string) => {},
    height = '300px',
    readOnly = false,
    lineWrapping = false,
    language = 'json'
  }: Props = $props();

  let editorContainer: HTMLElement | undefined = $state();
  let editorView: EditorView | undefined = $state();
  let prevReadOnly = $state(readOnly);
  let prevLineWrapping = $state(lineWrapping);

  // Get language extension based on language name
  function getLanguageExtension(language: string = 'json'): any {
    // For now we only support JSON
    return json();
  }

  // Create initial editor
  function setupEditor(): void {
    if (!editorContainer) return;
    
    // Clean up existing editor if any
    if (editorView) {
      editorView.destroy();
    }
    
    // Create read-only extension if needed
    const readOnlyExtension = readOnly ? EditorView.editable.of(false) : [];
    
    // Create line wrapping extension if needed
    const lineWrappingExtension = lineWrapping ? EditorView.lineWrapping : [];
    
    const startState = EditorState.create({
      doc: value,
      extensions: [
        basicSetup,
        getLanguageExtension(language),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            const newValue = update.state.doc.toString();
            onChange(newValue);
          }
        }),
        readOnlyExtension,
        lineWrappingExtension
      ]
    });

    editorView = new EditorView({
      state: startState,
      parent: editorContainer
    });
    
    // Update previous values
    prevReadOnly = readOnly;
    prevLineWrapping = lineWrapping;
  }

  onMount(() => {
    setupEditor();
  });

  onDestroy(() => {
    if (editorView) {
      editorView.destroy();
    }
  });

  export function updateContent(newValue: string): void {
    if (editorView && newValue !== editorView.state.doc.toString()) {
      editorView.dispatch({
        changes: {
          from: 0,
          to: editorView.state.doc.length,
          insert: newValue
        }
      });
    }
  }

  // Format JSON content
  export function formatJson(): void {
    if (!editorView) return;
    
    try {
      const content = editorView.state.doc.toString();
      const parsed = JSON.parse(content);
      const formatted = JSON.stringify(parsed, null, 2);
      
      if (content !== formatted) {
        updateContent(formatted);
      }
    } catch (error) {
      // Ignore formatting errors
      console.error("JSON formatting error:", error);
    }
  }

  // Update content reactively when value prop changes
  $effect(() => {
    if (editorView && value !== editorView.state.doc.toString()) {
      updateContent(value);
    }
  });

  // Watch for readOnly or lineWrapping changes
  $effect(() => {
    // Only rebuild editor if these props have changed
    if (editorView && (readOnly !== prevReadOnly || lineWrapping !== prevLineWrapping)) {
      setupEditor();
    }
  });
</script>

<div class="json-editor-container" bind:this={editorContainer} style="height: {height}"></div>

<style>
  .json-editor-container {
    border: 1px solid var(--border-color, var(--b3, #ddd));
    border-radius: var(--rounded-box, 0.5rem);
    overflow: hidden;
  }

  :global(.json-editor-container .cm-editor) {
    height: 100%;
  }

  :global(.json-editor-container .cm-scroller) {
    overflow: auto;
    height: 100%;
  }
</style>