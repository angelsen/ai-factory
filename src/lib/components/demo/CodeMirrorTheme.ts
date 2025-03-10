import { EditorView } from 'codemirror';
import { tags } from '@lezer/highlight';
import { HighlightStyle, syntaxHighlighting } from '@codemirror/language';

// Dark theme lists from various popular dark themes
const DARK_THEMES = [
  'dark', 'synthwave', 'halloween', 'forest', 'black', 'dracula', 
  'night', 'coffee', 'business', 'luxury', 'dracula', 'emerald'
];

// Determine if current theme is dark
export function isDarkTheme(themeName: string): boolean {
  return DARK_THEMES.includes(themeName.toLowerCase());
}

// Get current theme name
export function getCurrentTheme(): string {
  if (typeof document === 'undefined') return 'light';
  return document.documentElement.getAttribute('data-theme') || 'light';
}

// Create editor base theme
export function createEditorTheme(themeName = getCurrentTheme()): any {
  const isDark = isDarkTheme(themeName);
  
  return EditorView.theme({
    '&': {
      backgroundColor: 'var(--b1)',
      color: 'var(--bc)',
    },
    '.cm-content': {
      caretColor: 'var(--p)',
      fontFamily: 'var(--font-mono, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace)',
      padding: '10px 0'
    },
    '.cm-cursor': {
      borderLeftColor: 'var(--p)',
      borderLeftWidth: '2px'
    },
    '.cm-activeLine': {
      backgroundColor: isDark 
        ? 'color-mix(in srgb, var(--b1) 85%, var(--bc))' 
        : 'color-mix(in srgb, var(--b1) 95%, var(--bc))'
    },
    '.cm-gutters': {
      backgroundColor: 'var(--b2)',
      color: 'var(--bc)',
      border: 'none',
      borderRight: '1px solid var(--b3)'
    },
    '.cm-activeLineGutter': {
      backgroundColor: isDark 
        ? 'color-mix(in srgb, var(--b2) 85%, var(--bc))' 
        : 'color-mix(in srgb, var(--b2) 95%, var(--bc))'
    },
    '.cm-selectionBackground': {
      backgroundColor: 'color-mix(in srgb, var(--p) 30%, transparent)',
    },
    '&.cm-focused .cm-selectionBackground': {
      backgroundColor: 'color-mix(in srgb, var(--p) 40%, transparent)',
    },
    '.cm-foldPlaceholder': {
      backgroundColor: 'var(--p)',
      color: 'var(--pc)',
      border: 'none',
      borderRadius: 'var(--rounded-btn, 0.5rem)',
    },
    '.cm-tooltip': {
      backgroundColor: 'var(--b2)',
      color: 'var(--bc)',
      border: '1px solid var(--b3)',
      borderRadius: 'var(--rounded-box, 0.5rem)',
    },
    '.cm-tooltip-autocomplete': {
      '& > ul > li[aria-selected]': {
        backgroundColor: 'var(--p)',
        color: 'var(--pc)',
      },
    },
    '.cm-panels': {
      backgroundColor: 'var(--b2)',
      color: 'var(--bc)',
    },
    '.cm-panels-top': {
      borderBottom: '1px solid var(--b3)',
    },
    '.cm-panels-bottom': {
      borderTop: '1px solid var(--b3)',
    },
    '.cm-button': {
      backgroundColor: 'var(--b3)',
      color: 'var(--bc)',
      border: 'none',
      borderRadius: 'var(--rounded-btn, 0.5rem)',
      '&:hover': {
        backgroundColor: 'var(--b3)',
      },
    },
    '.cm-textfield': {
      backgroundColor: 'var(--b1)',
      border: '1px solid var(--b3)',
      borderRadius: 'var(--rounded-btn, 0.5rem)',
    },
  }, { dark: isDark });
}

// Create syntax highlighting for various languages
export function createSyntaxHighlighting(themeName = getCurrentTheme()): any {
  const isDark = isDarkTheme(themeName);
  
  const highlightStyle = HighlightStyle.define([
    // JSON specific
    { tag: tags.propertyName, color: 'var(--s)' },   // Property names (keys)
    { tag: tags.string, color: 'var(--su)' },       // String values
    { tag: tags.number, color: 'var(--er)' },       // Numbers
    { tag: tags.bool, color: 'var(--wa)' },         // Booleans
    { tag: tags.null, color: 'var(--in)' },         // Null values
    
    // General purpose
    { tag: tags.keyword, color: 'var(--p)' },
    { tag: tags.comment, color: 'var(--n)', fontStyle: 'italic' },
    { tag: tags.definition(tags.variableName), color: 'var(--s)' },
    { tag: tags.function(tags.variableName), color: 'var(--a)' },
    { tag: tags.className, color: 'var(--s)' },
    { tag: tags.attributeName, color: 'var(--s)' },
    { tag: tags.literal, color: 'var(--er)' },
    { tag: tags.typeName, color: 'var(--s)' },
    { tag: tags.heading, color: 'var(--p)', fontWeight: 'bold' },
    { tag: tags.emphasis, fontStyle: 'italic' },
    { tag: tags.strong, fontWeight: 'bold' },
    
    // Braces and delimiters
    { tag: tags.brace, color: 'var(--bc)' },
    { tag: tags.bracket, color: 'var(--bc)' },
    { tag: tags.punctuation, color: 'var(--bc)' },
    { tag: tags.paren, color: 'var(--bc)' },
  ]);
  
  return syntaxHighlighting(highlightStyle);
}

// Create a complete theme extension
export function createTheme(themeName = getCurrentTheme()): any[] {
  return [
    createEditorTheme(themeName),
    createSyntaxHighlighting(themeName)
  ];
}

// Listen for theme changes
export function createThemeWatcher(callback: (themeName: string) => void): () => void {
  if (typeof document === 'undefined') return () => {};
  
  const htmlElement = document.documentElement;
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
        const newTheme = htmlElement.getAttribute('data-theme') || 'light';
        callback(newTheme);
      }
    });
  });
  
  observer.observe(htmlElement, { attributes: true });
  
  // Return disconnect function
  return () => observer.disconnect();
}