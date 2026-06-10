export const ERNI_THEME = {
  slideWidth: 13.33,
  slideHeight: 7.5,

  font: "Source Sans Pro",
  fallbackFont: "Arial",

  colors: {
    erniBlue: "033778",
    cyan: "00AADB",
    darkGray: "3C3C3B",
    lightGray: "B1B0B1",
    white: "FFFFFF",
  },

  footer: {
    text: "Better ask ERNI",
    position: { x: 0.4, y: 0.2 },
    slideNumberPosition: { x: 12.4, y: 0.2 },
    fontSize: 8,
  },
} as const;

export type ErniTheme = typeof ERNI_THEME;
