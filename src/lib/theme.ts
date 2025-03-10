// Available themes from app.css
// Base themes are handled specially in ThemeController
export const BASE_THEMES = ['light', 'dark', 'system'];

// All available themes (add new themes here)
export const AVAILABLE_THEMES = ['light', 'dark', 'synthwave', 'cupcake', 'cyberpunk'];

// Only additional themes (excluding base themes)
export const ADDITIONAL_THEMES = AVAILABLE_THEMES.filter(theme => !BASE_THEMES.includes(theme) || theme === 'system');

// This function initializes the theme based on localStorage and system preference
export function initTheme(): void {
  // Only run in browser environment
  if (typeof window === 'undefined') return;

  // Script to run in the client
  const themeInitScript = `
    (function() {
      // Import available themes dynamically
      const AVAILABLE_THEMES = ${JSON.stringify(AVAILABLE_THEMES)};
      
      // Get theme from localStorage or default to system preference
      const storedTheme = localStorage.getItem('theme');
      
      if (storedTheme && storedTheme !== 'system') {
        // Use explicitly set preference if it's a valid theme
        if (AVAILABLE_THEMES.includes(storedTheme)) {
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