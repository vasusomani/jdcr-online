/** @type {import('tailwindcss').Config} */
import colors from "tailwindcss/colors";

module.exports = {
  content: ["./templates/**/*.html", "./core/templates/**/*.html", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
    container: {
      center: true,
      padding: {
        DEFAULT: "1rem",
        sm: "2rem",
        lg: "4rem",
        xl: "5rem",
        "2xl": "6rem",
      },
      screens: {
        sm: '600px',
        md: '728px',
        lg: '984px',
        xl: '1240px',
        '2xl': '1496px',
      },
    },
    colors: {
      primary: "#3EADC1",      
      primaryHover: "#2A8699",
      secondary: "#5EBE9E",
      tertiary: "#A7D397",     
      light: "#F6FAFB",
      black: colors.black,
      white: colors.white,
      amber: colors.amber,
      emerald: colors.emerald,
      indigo: colors.indigo,
      yellow: colors.yellow,
      stone: colors.stone,
      sky: colors.sky,
      neutral: colors.neutral,
      gray: colors.gray,
      slate: colors.slate,
      red: colors.red,
      lime: colors.lime,
      teal: colors.teal,
      cyan: colors.cyan
    },
  },
  plugins: [require("flowbite/plugin")],
  important: true,
};
