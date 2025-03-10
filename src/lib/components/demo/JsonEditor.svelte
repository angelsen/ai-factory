<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, basicSetup } from 'codemirror';
  import { EditorState } from '@codemirror/state';
  import { json } from '@codemirror/lang-json';

  export let value = '';
  export let onChange = (val: string) => {};
  export let height = '300px';

  let editorContainer: HTMLElement;
  let editorView: EditorView;

  onMount(() => {
    if (editorContainer) {
      const startState = EditorState.create({
        doc: value,
        extensions: [
          basicSetup,
          json(),
          EditorView.updateListener.of((update) => {
            if (update.docChanged) {
              const newValue = update.state.doc.toString();
              onChange(newValue);
            }
          })
        ]
      });

      editorView = new EditorView({
        state: startState,
        parent: editorContainer
      });
    }
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

  $: if (editorView && value !== editorView.state.doc.toString()) {
    updateContent(value);
  }
</script>

<div class="json-editor-container" bind:this={editorContainer} style="height: {height}"></div>

<style>
  .json-editor-container {
    border: 1px solid var(--border-color, #ddd);
    border-radius: 0.25rem;
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