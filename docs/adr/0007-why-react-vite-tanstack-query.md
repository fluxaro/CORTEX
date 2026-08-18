# ADR 0007: Why React + Vite + TanStack Query

## Status
Accepted

## Context
Cortex requires a rich, interactive SaaS frontend with complex data visualizations (dependency graphs, radar charts, trend lines), real-time polling for analysis status, and a responsive, accessible UI.

## Decision
Use **React 18** with **Vite**, **TypeScript**, **TanStack Query v5**, and **Tailwind CSS**.

## Rationale

### React 18
- Concurrent rendering enables responsive UI during heavy chart rendering.
- Largest ecosystem of data visualization libraries (Recharts, React Flow).
- React Suspense enables clean loading state management for API data.

### Vite
- 10–50x faster dev server HMR compared to Create React App / Webpack.
- Native ESM-based dev build with optimized tree-shaking for production.
- First-class TypeScript support without extra configuration.

### TanStack Query v5
- Automatic background refetching for polling analysis status without manual `setInterval`.
- Built-in caching eliminates redundant API calls when navigating between pages.
- Optimistic updates and mutation state management for form submissions.

### Tailwind CSS
- Utility-first approach enables rapid UI iteration without context-switching to CSS files.
- JIT compiler produces minimal production CSS bundle.
- Custom design system tokens in `tailwind.config.js` for the dark glassmorphic aesthetic.

## Alternatives Considered
| Alternative | Rejection Reason |
| :--- | :--- |
| Next.js | Server-side rendering unnecessary for an authenticated SaaS dashboard |
| Vue 3 | Smaller ecosystem for complex visualization libraries |
| Angular | Heavier framework with steeper learning curve; overkill for this scope |
| SWR | Less feature-rich than TanStack Query; no mutation management |

## Consequences
- No server-side rendering — all routing is client-side.
- The frontend is a pure Single Page Application deployed as static files.
