import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'nomadWheels': '#80CBC4',
        'nomadWheels-dark': '#00382D'
      },
    },
  },
  plugins: [],
} satisfies Config;
