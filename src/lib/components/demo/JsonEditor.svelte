<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, basicSetup } from 'codemirror';
  import { EditorState } from '@codemirror/state';
  import { json } from '@codemirror/lang-json';
  import { 
    createTheme, 
    createThemeWatcher, 
    getCurrentTheme
  } from './CodeMirrorTheme';

  export let value = '';
  export let onChange = (val: string) => {};
  export let height = '300px';
  export let readOnly = false;
  export let lineWrapping = false;

  let editorContainer: HTMLElement;
  let editorView: EditorView;
  let disconnectThemeWatcher: () => void;

  // Handle theme changes
  function handleThemeChange(themeName: string): void {
    if (!editorView) return;
    
    // Re-initialize the editor with the new theme
    const content = editorView.state.doc.toString();
    editorView.destroy();
    
    const startState = EditorState.create({
      doc: content,
      extensions: [
        basicSetup,
        json(),
        ...createTheme(themeName),
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            const newValue = update.state.doc.toString();
            onChange(newValue);
          }
        }),
        readOnly ? EditorView.editable.of(false) : [],
        lineWrapping ? EditorView.lineWrapping : []
      ]
    });

    editorView = new EditorView({
      state: startState,
      parent: editorContainer
    });
  }

  onMount(() => {
    if (editorContainer) {
      // Get initial theme
      const initialTheme = getCurrentTheme();

      // Create read-only extension if needed
      const readOnlyExtension = readOnly ? EditorView.editable.of(false) : [];
      
      // Create line wrapping extension if needed
      const lineWrappingExtension = lineWrapping ? EditorView.lineWrapping : [];
      
      const startState = EditorState.create({
        doc: value,
        extensions: [
          basicSetup,
          json(),
          ...createTheme(initialTheme),
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
      
      // Set up theme watcher
      disconnectThemeWatcher = createThemeWatcher(handleThemeChange);
    }
  });

  onDestroy(() => {
    if (editorView) {
      editorView.destroy();
    }
    
    if (disconnectThemeWatcher) {
      disconnectThemeWatcher();
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
  $: if (editorView && value !== editorView.state.doc.toString()) {
    updateContent(value);
  }
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

  /* Add smooth transitions between themes */
  :global(.json-editor-container *) {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
  }
</style>