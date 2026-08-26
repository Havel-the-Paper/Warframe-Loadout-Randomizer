/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        orokin: {
          50: '#fbf9eb',
          100: '#f5f0ce',
          200: '#ece09c',
          300: '#e1ca63',
          400: '#d7b438',
          500: '#c59d24',
          600: '#a77c1b',
          700: '#855d19',
          800: '#6f4a1a',
          900: '#5e3e1b',
          950: '#37210c',
        },
        void: {
          900: '#070a12',
          950: '#030509',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(215, 180, 56, 0.4), inset 0 0 5px rgba(215, 180, 56, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(215, 180, 56, 0.8), inset 0 0 10px rgba(215, 180, 56, 0.4)' },
        }
      }
    },
  },
  plugins: [],
}
