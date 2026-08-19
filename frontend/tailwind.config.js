import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#070b14",
        panel: "#101726",
        accent: "#7c5cff",
        aqua: "#33d6c7",
      },
      boxShadow: {
        glow: "0 0 40px rgba(124, 92, 255, 0.17)",
      },
    },
  },
  plugins: [typography],
};
