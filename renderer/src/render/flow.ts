import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { addFooter, addIcon, addSeparatorLine } from "./helpers.js";

export function renderFlowLayout3b(
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

  const steps = content.steps ?? [];
  const stepCount = Math.min(steps.length, 5);
  const totalW = 11.73;
  const gap = 0.2;
  const colWidth = (totalW - (stepCount - 1) * gap) / stepCount;
  const startX = 0.8;
  const startY = 2.5;

  for (let i = 0; i < stepCount; i++) {
    const x = startX + i * (colWidth + gap);

    slide.addShape("ellipse", {
      x: x + colWidth / 2 - 0.3,
      y: startY,
      w: 0.6,
      h: 0.6,
      fill: { color: ERNI_THEME.colors.erniBlue },
    });

    slide.addText(steps[i].number ?? String(i + 1), {
      x: x + colWidth / 2 - 0.3,
      y: startY,
      w: 0.6,
      h: 0.6,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.white,
      bold: true,
      align: "center",
      valign: "middle",
    });

    if (i < stepCount - 1) {
      slide.addShape("line", {
        x: x + colWidth + 0.02,
        y: startY + 0.3,
        w: gap - 0.04,
        h: 0,
        line: { color: ERNI_THEME.colors.erniBlue, width: 1.5 },
      });
    }

    slide.addText(steps[i].title, {
      x,
      y: startY + 0.8,
      w: colWidth,
      h: 0.5,
      fontSize: 13,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      align: "center",
    });

    slide.addText(steps[i].description, {
      x,
      y: startY + 1.4,
      w: colWidth,
      h: 2.8,
      fontSize: 11,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}
