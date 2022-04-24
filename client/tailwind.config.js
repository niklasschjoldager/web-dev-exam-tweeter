const plugin = require("tailwindcss/plugin")

const backfaceVisibility = plugin(function ({ addUtilities }) {
  addUtilities({
    ".backface-visible": {
      "backface-visibility": "visible",
    },
    ".backface-hidden": {
      "backface-visibility": "hidden",
    },
  })
})

const hyphens = plugin(function ({ addUtilities }) {
  addUtilities({
    ".hyphens-none": {
      hyphens: "none",
    },
    ".hyphens-auto": {
      hyphens: "auto",
    },
    ".hyphens-manual": {
      hyphens: "manual",
    },
  })
})

module.exports = {
  mode: "JIT",
  content: ["../views/**/*.{html,js}"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      white: "hsl(0, 0%, 100%)",
      black: {
        100: "hsl(207, 10%, 17%)",
        200: "hsl(213, 27%, 8%)",
      },
      primary: {
        100: "hsl(204, 79%, 47%)",
        200: "hsl(204, 88%, 53%)",
      },
      gray: {
        100: "hsl(180, 12%, 97%)",
        200: "hsl(192, 20%, 95%)",
        300: "hsl(199, 20%, 84%)",
        400: "hsl(206, 15%, 38%)",
        500: "hsl(207, 10%, 17%)",
      },
      success: "hsl(160, 100%, 36%)",
      danger: {
        100: "hsl(357, 76%, 49%)",
        200: "hsl(356, 91%, 54%)",
      },
    },
    screens: {
      xs: "500px",
      sm: "640px",
      md: "768px",
      lg: "988px",
      xl: "1264px",
      "2xl": "1536px",
      minHminW: { raw: "(min-height: 640px) and (min-width: 640px)" },
    },
    extend: {
      boxShadow: {
        focus: "0px 0px 0px 1px hsl(204, 88%, 53%)",
      },
    },
  },
  plugins: [backfaceVisibility, hyphens],
}
