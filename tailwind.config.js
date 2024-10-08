/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      colors: {
        'lightblue': '#edf2f7',
      },
    },
  },
  plugins: [],
}

