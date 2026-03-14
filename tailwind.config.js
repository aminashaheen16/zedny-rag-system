/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Zedny.ai inspired Deep Purple/Indigo Palette
        primary: {
          DEFAULT: '#6366F1', // Indigo 500
          50: '#EEF2FF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A5B4FC',
          400: '#818CF8',
          500: '#6366F1',
          600: '#4F46E5', // Indigo 600 - Main Brand Color
          700: '#4338CA',
          800: '#3730A3',
          900: '#312E81',
          950: '#1E1B4B', // Deepest Indigo for backgrounds
        },
        // Secondary/Neutral for Dark Theme
        secondary: {
          DEFAULT: '#1E293B',
          50: '#F8FAFC',
          100: '#F1F5F9',
          200: '#E2E8F0',
          300: '#CBD5E1',
          400: '#94A3B8',
          500: '#64748B',
          600: '#475569',
          700: '#334155',
          800: '#1E293B', // Slate 800
          900: '#0F172A', // Slate 900 - Dark Background
          950: '#020617', // Almost Black
        },
        // Dark Theme Background Surface Colors
        dark: {
          bg: '#0F172A', // Main background
          card: '#1E293B', // Card background
          hover: '#334155',
          border: '#334155',
        },
        accent: {
          purple: '#8B5CF6',
          cyan: '#06B6D4',
          glow: 'rgba(99, 102, 241, 0.5)', // Indigo Glow
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '"Outfit"', 'system-ui', 'sans-serif'],
        display: ['"Outfit"', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-gradient': 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #030712 100%)', // Deep Purple to Black
        'glow-conic': 'conic-gradient(from 180deg at 50% 50%, #6366f1 0deg, #a855f7 180deg, #ec4899 360deg)',
      },
      boxShadow: {
        'glow': '0 0 20px rgba(99, 102, 241, 0.25)',
        'glow-lg': '0 0 40px rgba(99, 102, 241, 0.35)',
        'soft': '0 10px 40px -10px rgba(0,0,0,0.5)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
