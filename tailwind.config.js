/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    "opendating/**/*.html",
    "opendating/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Raleway', 'sans-serif']
      },
      colors: {
        'accent': {
          '50': '#fff6ed',
          '100': '#ffebd4',
          '200': '#ffd3a8',
          '300': '#ffb370',
          '400': '#ff8737',
          '500': '#ff630b',
          '600': '#f04b06',
          '700': '#c73607',
          '800': '#9e2b0e',
          '900': '#7f270f',
          '950': '#451005',
        },
        'neutral': {
          50: '#FAFAFA',
          100: '#ECECEC',
          200: '#D0D0D0',
          300: '#B4B4B4',
          400: '#989898',
          500: '#7C7C7C',
          600: '#626262',
          700: '#494949',
          800: '#2F2F2F',
          900: '#161616',
          950: '#090909'
        },

      },
    },
  },
  plugins: [],
}

