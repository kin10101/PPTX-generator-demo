import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { addFooter } from "./helpers.js";

export function renderContainersLayout(
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

  const metrics = content.metrics ?? [];
  const count = Math.min(metrics.length, 6);
  const cols = 3;
  const boxW = 3.6;
  const boxH = 2.2;
  const startX = 0.8;
  const startY = 1.8;
  const gapX = 0.35;
  const gapY = 0.35;

  for (let i = 0; i < count; i++) {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (boxW + gapX);
    const y = startY + row * (boxH + gapY);

    slide.addShape("rect", {
      x,
      y,
      w: boxW,
      h: boxH,
      fill: { color: "F5F5F5" },
      rectRadius: 0.05,
    });

    slide.addText(metrics[i].value, {
      x,
      y: y + 0.3,
      w: boxW,
      h: 0.9,
      fontSize: 34,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      align: "center",
      valign: "middle",
    });

    slide.addText(metrics[i].label, {
      x,
      y: y + 1.2,
      w: boxW,
      h: 0.8,
      fontSize: 13,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}
