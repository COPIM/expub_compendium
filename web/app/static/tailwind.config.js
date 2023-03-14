module.exports = {
  mode: 'jit',
  content: [
    '../templates/*.html'
  ],
  theme: {
    extend: {
      fontSize: {
        // xs: ['0.95rem', { lineHeight: '1.35' }],
        sm: ['0.95rem', { lineHeight: '1.35' }],
        base: ['1.08rem', { lineHeight: '1.35' }],
        // lg: ['1.125rem', { lineHeight: '1.5' }],
        // xl: ['1.25rem', { lineHeight: '1.6' }],
        // '2xl': ['1.5rem', { lineHeight: '1.88rem' }],
        // '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.53rem', { lineHeight: '1' }],
        // '5xl': ['3rem', { lineHeight: '1.1' }],
        // '6xl': ['3.75rem', { lineHeight: '1.04' }],
        // '7xl': ['4.5rem', { lineHeight: '1.1' }],
        // '8xl': ['6rem', { lineHeight: '1' }],
        // '9xl': ['8rem', { lineHeight: '1' }],
      },
      colors: {
        // 'ggreen': {
        //   light: '#67e8f9',
        //   DEFAULT: 'var(--primary-color)',
        //   dark: '#0e7490',
        // },
      },
    }
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
