import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { addFooter, addIcon } from "./helpers.js";

export function renderPeopleLayout1(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: 0.8,
    y: 0.7,
    w: 11.73,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  const options = content.options ?? [];
  const count = Math.min(options.length, 3);
  const colWidth = 3.6;
  const startX = 0.8;
  const startY = 2.0;
  const gap = 0.4;

  for (let i = 0; i < count; i++) {
    const x = startX + i * (colWidth + gap);

    slide.addShape("ellipse", {
      x: x + colWidth / 2 - 0.65,
      y: startY,
      w: 1.3,
      h: 1.3,
      fill: { color: "E8E8E8" },
    });

    slide.addText(options[i].title, {
      x,
      y: startY + 1.5,
      w: colWidth,
      h: 0.5,
      fontSize: 15,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      align: "center",
    });

    slide.addText(options[i].description, {
      x,
      y: startY + 2.1,
      w: colWidth,
      h: 2.4,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}
