import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";

export function renderSectionLayout1(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.background = { color: ERNI_THEME.colors.erniBlue };

  const sectionNum = content.subtitle ?? String(slideNumber);
  slide.addText(sectionNum, {
    x: 1.0,
    y: 2.0,
    w: 3.5,
    h: 3.5,
    fontSize: 72,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.white,
    bold: true,
    valign: "middle",
    align: "center",
    autoFit: true,
  });

  slide.addText(content.title, {
    x: 5.0,
    y: 2.5,
    w: 7.5,
    h: 2.5,
    fontSize: 32,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.white,
    bold: true,
    valign: "middle",
    autoFit: true,
  });
}
