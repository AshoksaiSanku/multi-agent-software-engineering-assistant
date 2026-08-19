# Lesson-17: Frontend Foundation - Vite, React, Tailwind, Providers, Layout

## Objective

Create the frontend application foundation.

## Files Created

```text
frontend/package.json
frontend/index.html
frontend/vite.config.js
frontend/tailwind.config.js
frontend/postcss.config.js
frontend/eslint.config.js
frontend/Dockerfile
frontend/src/main.jsx
frontend/src/App.jsx
frontend/src/index.css
frontend/src/lib/api.js
frontend/src/contexts/AuthContext.jsx
frontend/src/contexts/ThemeContext.jsx
frontend/src/contexts/ToastContext.jsx
frontend/src/components/Shell.jsx
frontend/src/components/Ui.jsx
frontend/src/components/Markdown.jsx
```

## Knowledge Required

- **JavaScript**: Browser programming language.
- **JSX**: JavaScript syntax for React UI.
- **React component**: Reusable UI function.
- **React hook**: Function like `useState` or `useEffect`.
- **Context provider**: Shares global state.
- **React Router**: Client-side page routing.
- **Tailwind CSS**: Utility class styling.
- **Vite**: Fast dev/build tool.

## Data Flow

Browser loads `index.html` -> `main.jsx` mounts React -> providers wrap app -> `App.jsx` chooses route -> `Shell` renders protected layout.

## Common Mistakes

- Forgetting provider order.
- Missing Tailwind content globs.
- Incorrect API URL.
- Storing secrets in frontend code.

## Verification

Run frontend dev server and see login page.

