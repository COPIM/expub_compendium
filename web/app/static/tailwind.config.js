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
        base: ['1.1rem', { lineHeight: '1.22' }],
        lg: ['1.24rem', { lineHeight: '1.1' }],
        xl: ['1.5rem', { lineHeight: '1.1' }],
        '2xl': ['1.85rem', { lineHeight: '1' }],
        '3xl': ['2rem', { lineHeight: '1' }],
        '4xl': ['3rem', { lineHeight: '1' }],
        '5xl': ['4.2rem', { lineHeight: '0.9' }],
        // '6xl': ['3.75rem', { lineHeight: '1.04' }],
        // '7xl': ['4.5rem', { lineHeight: '1.1' }],
        // '8xl': ['6rem', { lineHeight: '1' }],
        // '9xl': ['8rem', { lineHeight: '1' }],
      },
      colors: {
        'expurple': {
          DEFAULT: 'rgba(103, 48, 255,0.5)'
        }
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
