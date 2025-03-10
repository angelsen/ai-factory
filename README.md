# SvelteKit Starter Kit

A comprehensive starter template for modern SvelteKit applications with essential integrations.

[View tagged release (2025-03-10)](https://github.com/angelsen/ai-factory/tree/2025-03-10)

## Features

- **SvelteKit**: Modern Svelte framework with server-side rendering
- **DaisyUI v5**: Component library for Tailwind CSS with theming
- **Lucide**: Beautiful, consistent icon set
- **Lucia**: Authentication framework
- **Drizzle ORM**: Lightweight TypeScript ORM for SQL databases

## Quick Start

```bash
# Clone the repository (specific release version)
git clone -b 2025-03-10 https://github.com/angelsen/ai-factory.git my-app

# Navigate to project
cd my-app

# Install dependencies
npm install

# Set up the database
npm run db:push

# Start development server
npm run dev -- --open
```

## Included Components

### UI Components
- Fully typed and accessible UI components in `src/lib/components/ui`
- Responsive Navbar with mobile menu
- Card component with variants
- Button component with multiple styles
- Theme controller with light/dark and custom themes

### Authentication
- Lucia auth integration
- Login form and user profile components
- Authentication API routes

### Database
- Drizzle ORM setup
- SQLite database for development
- Schema definitions

## Theme System

The starter includes a comprehensive theme system:
- Light/dark mode toggle
- System preference detection
- Custom theme selection
- Theme persistence with localStorage

## Customization

### Adding New Components
Place new UI components in `src/lib/components/ui/`. Follow the existing pattern for TypeScript typing and props.

### Modifying Themes
Edit theme configurations in `src/app.css` and `src/lib/theme.ts`.

### Database Schema
Modify the database schema in `src/lib/server/db/schema.ts`.

## Building and Deployment

```bash
# Build the application
npm run build

# Preview the production build
npm run preview
```

## License

MIT

---

Made with ♥ by Fredrik Angelsen