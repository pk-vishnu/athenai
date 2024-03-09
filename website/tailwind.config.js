/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins'],
      },
      colors: {
        'dark': '#131314',
        'light':'#c4c3ce',
        'semi-dark':'#333537',
        'primary':'#edab74',
        'secondary':'#edab74',
        'altdark':'#210102',
      },
    },
  },
  plugins: [],
}

