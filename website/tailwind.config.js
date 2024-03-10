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
      animation: {
        typewriter: 'typewriter 2s steps(45) forwards',
        caret: 'typewriter 2s steps(45) forwards, blink 1s steps(4) infinite 2s',
      },
      keyframes: {
        typewriter: {
          to: {
            left: '100%',
          },
        },
        blink: {
          '0%': {
            opacity: '0',
          },
          '0.1%': {
            opacity: '1',
          },
          '50%': {
            opacity: '1',
          },
          '50.1%': {
            opacity: '0',
          },
          '100%': {
            opacity: '0',
          },
        },
      },
    },
  },
  plugins: [],
}

