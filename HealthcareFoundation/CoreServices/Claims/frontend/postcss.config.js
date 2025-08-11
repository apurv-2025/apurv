// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? {
      '@fullhuman/postcss-purgecss': {
        content: [
          './src/**/*.{js,jsx,ts,tsx}',
          './public/index.html',
        ],
        defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
        safelist: [
          /^bg-/,
          /^text-/,
          /^border-/,
          /^hover:/,
          /^focus:/,
          /^active:/,
          /^animate-/,
          'status-badge',
        ]
      },
      cssnano: {
        preset: 'default',
      },
    } : {}),
  },
}
