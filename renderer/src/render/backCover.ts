import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";

export function renderBackCover1(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.background = { color: ERNI_THEME.colors.white };

  slide.addText(content.title, {
    x: 1.0,
    y: 2.5,
    w: 11.33,
    h: 1.0,
    fontSize: 28,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
    align: "center",
  });

  if (content.body) {
    slide.addText(content.body, {
      x: 2.5,
      y: 3.7,
      w: 8.33,
      h: 2.0,
      fontSize: 14,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }
}

export function renderBackCover2(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  slide.background = { color: ERNI_THEME.colors.erniBlue };

  slide.addText("E", {
    x: 4.0,
    y: 1.5,
    w: 5.33,
    h: 4.5,
    fontSize: 220,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.white,
    bold: true,
    align: "center",
    valign: "middle",
  });
}

export function renderBackCover3(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  slide.background = { color: ERNI_THEME.colors.erniBlue };

  slide.addText("ERNI", {
    x: 3.33,
    y: 2.8,
    w: 6.67,
    h: 2.0,
    fontSize: 56,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.white,
    bold: true,
    align: "center",
    valign: "middle",
  });
}
