import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { addFooter, addIcon, addSeparatorLine } from "./helpers.js";

export function renderChartLayout2a(
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

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: 0.8,
      y: 1.55,
      w: 11.73,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  const options = content.options ?? [];
  const colCount = Math.min(options.length, 3);
  const colWidth = 3.6;
  const startX = 0.8;
  const startY = 2.4;
  const gap = 0.4;

  for (let i = 0; i < colCount; i++) {
    const x = startX + i * (colWidth + gap);

    if (i > 0) {
      addSeparatorLine(slide, x - gap / 2, startY, 4.2);
    }

    if (data.icons && data.icons[i]) {
      addIcon(slide, data.icons[i], { x: x + colWidth / 2 - 0.35, y: startY, size: 0.7 });
    }

    slide.addText(options[i].title, {
      x,
      y: startY + 1.0,
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
      y: startY + 1.6,
      w: colWidth,
      h: 2.6,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}
