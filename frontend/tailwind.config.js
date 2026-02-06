/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pcna-primary': '#6366f1',
        'pcna-secondary': '#8b5cf6',
        'pcna-accent': '#ec4899',
        'pcna-dark': '#1e293b',
        'pcna-light': '#f1f5f9',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
