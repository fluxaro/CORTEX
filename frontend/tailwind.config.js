/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#f8fafc",
        surface: "#ffffff",
        "surface-card": "#ffffff",
        "surface-hover": "#f1f5f9",
        border: "#e2e8f0",
        "border-focus": "#2563eb",
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
        accent: {
          cyan: "#06b6d4",
          emerald: "#10b981",
          purple: "#8b5cf6",
          amber: "#f59e0b",
          rose: "#f43f5e",
        },
      },
      fontFamily: {
        display: ["Fredoka", "Outfit", "Plus Jakarta Sans", "sans-serif"],
        sans: ["Plus Jakarta Sans", "Inter", "-apple-system", "sans-serif"],
        mono: ["Fira Code", "JetBrains Mono", "monospace"],
      },
      boxShadow: {
        glow: "0 0 20px -5px rgba(59, 130, 246, 0.3)",
        "glow-emerald": "0 0 20px -5px rgba(16, 185, 129, 0.3)",
        "glow-purple": "0 0 20px -5px rgba(139, 92, 246, 0.3)",
        glass: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
      },
    },
  },
  plugins: [],
}
