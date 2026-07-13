/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        nexus: {
          bg: "#0D1117",
          panel: "#131A22",
          border: "#242C37",
          teal: "#5EEAD4",
          violet: "#B794F6",
          amber: "#F0B429",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
    },
  },
  plugins: [],
}
