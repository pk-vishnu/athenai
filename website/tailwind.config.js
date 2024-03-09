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
        'semi-dark':'#333537'
      },
    },
  },
  plugins: [],
}

