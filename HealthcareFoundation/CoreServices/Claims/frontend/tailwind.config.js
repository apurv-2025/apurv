// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        // Custom FHIR brand colors
        fhir: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // Healthcare status colors
        status: {
          active: '#10b981',
          draft: '#f59e0b',
          cancelled: '#ef4444',
          error: '#dc2626',
          complete: '#059669',
          pending: '#6366f1',
        }
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'pulse-slow': 'pulse 3s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 30px -5px rgba(0, 0, 0, 0.05)',
        'hard': '0 10px 40px -10px rgba(0, 0, 0, 0.15), 0 20px 50px -10px rgba(0, 0, 0, 0.1)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class', // only generate classes
    }),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    // Custom plugin for FHIR-specific utilities
    function({ addUtilities, addComponents, theme }) {
      addUtilities({
        '.text-balance': {
          'text-wrap': 'balance',
        },
        '.text-pretty': {
          'text-wrap': 'pretty',
        },
      })
      addComponents({
        '.btn': {
          '@apply px-4 py-2 rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2': {},
        },
        '.btn-primary': {
          '@apply btn bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500': {},
        },
        '.btn-secondary': {
          '@apply btn bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500': {},
        },
        '.btn-danger': {
          '@apply btn bg-red-600 text-white hover:bg-red-700 focus:ring-red-500': {},
        },
        '.btn-success': {
          '@apply btn bg-green-600 text-white hover:bg-green-700 focus:ring-green-500': {},
        },
        '.card': {
          '@apply bg-white rounded-lg shadow-soft p-6': {},
        },
        '.card-header': {
          '@apply border-b border-gray-200 pb-4 mb-4': {},
        },
        '.status-badge': {
          '@apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium': {},
        },
        '.form-input': {
          '@apply block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500': {},
        },
        '.form-select': {
          '@apply block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500': {},
        },
        '.table-auto-responsive': {
          '@apply min-w-full divide-y divide-gray-200 overflow-hidden': {},
        },
      })
    },
  ],
  future: {
    hoverOnlyWhenSupported: true,
  },
}
