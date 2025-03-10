// Available themes from app.css
const AVAILABLE_THEMES = ['light', 'dark', 'synthwave', 'cupcake'];

// This function initializes the theme based on localStorage and system preference
export function initTheme(): void {
  // Only run in browser environment
  if (typeof window === 'undefined') return;

  // Script to run in the client
  const themeInitScript = `
    (function() {
      // Get theme from localStorage or default to system preference
      const storedTheme = localStorage.getItem('theme');
      
      if (storedTheme && storedTheme !== 'system') {
        // Use explicitly set preference if it's a valid theme
        if (${JSON.stringify(AVAILABLE_THEMES)}.includes(storedTheme)) {
          document.documentElement.setAttribute('data-theme', storedTheme);
        }
      } else {
        // Use system preference (respects the --prefersdark flag from daisyUI config)
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        // daisyUI v5 handles this automatically with the --prefersdark flag
        // but we set it explicitly to ensure consistency
        document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      }
    })();
  `;

  // Create and inject script
  const script = document.createElement('script');
  script.textContent = themeInitScript;
  document.head.appendChild(script);
}

// Call this function from the layout file or hooks