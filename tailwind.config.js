/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    "open-dating/templates/**/*.html",
    "open-dating/static/src/**/*.js"
  ],
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
        'light': {
          '50': '#fafafa',
          '100': '#efefef',
          '200': '#dcdcdc',
          '300': '#bdbdbd',
          '400': '#989898',
          '500': '#7c7c7c',
          '600': '#656565',
          '700': '#525252',
          '800': '#464646',
          '900': '#3d3d3d',
          '950': '#292929',
        },

      },
    },
  },
  plugins: [],
}

