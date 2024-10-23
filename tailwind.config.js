/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Raleway', 'sans-serif']
      },
      colors: {
        'orange': {
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
      },
    },
  },
  plugins: [],
}

