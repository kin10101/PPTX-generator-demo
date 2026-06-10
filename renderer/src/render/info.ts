import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import {
  addFooter,
  addImageCover,
  addIcon,
  addSeparatorLine,
  getAssetPath,
} from "./helpers.js";

// Slide dimensions: 13.33" x 7.5" (LAYOUT_WIDE)
const MARGIN = 0.8;
const FULL_W = 11.73; // 13.33 - 2*MARGIN
const IMG_W = 6.0;
const TEXT_X = 6.5;
const TEXT_W = 6.0;

function renderInlineSteps(
  slide: PptxSlide,
  steps: Array<{ number?: string; title: string; description: string }>,
  startX: number,
  startY: number,
  totalW: number
): void {
  const count = Math.min(steps.length, 4);
  const gap = 0.25;
  const colW = (totalW - (count - 1) * gap) / count;

  for (let i = 0; i < count; i++) {
    const x = startX + i * (colW + gap);

    slide.addText(steps[i].number ?? String(i + 1), {
      x: x,
      y: startY,
      w: 0.4,
      h: 0.4,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.white,
      bold: true,
      align: "center",
      valign: "middle",
      shape: "ellipse",
      fill: { color: ERNI_THEME.colors.erniBlue },
    } as any);

    slide.addText(steps[i].title, {
      x: x + 0.5,
      y: startY,
      w: colW - 0.55,
      h: 0.4,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      valign: "middle",
    });

    slide.addText(steps[i].description, {
      x,
      y: startY + 0.55,
      w: colW,
      h: 1.8,
      fontSize: 11,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
  }
}

function renderInlineOptions(
  slide: PptxSlide,
  options: Array<{ title: string; description: string }>,
  startX: number,
  startY: number,
  totalW: number
): void {
  const count = Math.min(options.length, 4);
  const gap = 0.25;
  const colW = (totalW - (count - 1) * gap) / count;

  for (let i = 0; i < count; i++) {
    const x = startX + i * (colW + gap);

    slide.addShape("rect", {
      x,
      y: startY,
      w: colW,
      h: 2.2,
      fill: { color: "F5F5F5" },
      rectRadius: 0.05,
    });

    slide.addText(options[i].title, {
      x: x + 0.15,
      y: startY + 0.15,
      w: colW - 0.3,
      h: 0.5,
      fontSize: 13,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      valign: "middle",
    });

    slide.addText(options[i].description, {
      x: x + 0.15,
      y: startY + 0.7,
      w: colW - 0.3,
      h: 1.35,
      fontSize: 11,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
  }
}

function renderInlineMetrics(
  slide: PptxSlide,
  metrics: Array<{ value: string; label: string }>,
  startX: number,
  startY: number,
  totalW: number
): void {
  const count = Math.min(metrics.length, 4);
  const gap = 0.2;
  const colW = (totalW - (count - 1) * gap) / count;

  for (let i = 0; i < count; i++) {
    const x = startX + i * (colW + gap);

    slide.addText(metrics[i].value, {
      x,
      y: startY,
      w: colW,
      h: 0.8,
      fontSize: 28,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
      align: "center",
      valign: "middle",
    });

    slide.addText(metrics[i].label, {
      x,
      y: startY + 0.8,
      w: colW,
      h: 0.6,
      fontSize: 11,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
      valign: "top",
    });
  }
}

export function renderInfoLayout5a(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: MARGIN,
    y: 0.7,
    w: FULL_W,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: MARGIN,
      y: 1.55,
      w: FULL_W,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  let nextY = 2.3;

  if (content.body) {
    slide.addText(content.body, {
      x: MARGIN,
      y: nextY,
      w: FULL_W,
      h: 1.6,
      fontSize: 14,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
    nextY += 1.8;
  }

  if (content.steps && content.steps.length > 0) {
    renderInlineSteps(slide, content.steps, MARGIN, nextY, FULL_W);
  } else if (content.options && content.options.length > 0) {
    renderInlineOptions(slide, content.options, MARGIN, nextY, FULL_W);
  } else if (content.metrics && content.metrics.length > 0) {
    renderInlineMetrics(slide, content.metrics, MARGIN, nextY, FULL_W);
  }

  addFooter(slide, slideNumber);
}

export function renderInfoLayout5b(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: MARGIN,
    y: 0.7,
    w: FULL_W,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: MARGIN,
      y: 1.55,
      w: FULL_W,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  if (content.body) {
    const parts = content.body.split("\n\n");
    const col1 = parts[0] ?? "";
    const col2 = parts.slice(1).join("\n\n");
    const colW = 5.6;

    slide.addText(col1, {
      x: MARGIN,
      y: 2.3,
      w: colW,
      h: 4.2,
      fontSize: 13,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });

    slide.addText(col2, {
      x: MARGIN + colW + 0.5,
      y: 2.3,
      w: colW,
      h: 4.2,
      fontSize: 13,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}

export function renderInfoLayout6a(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  if (data.image) {
    addImageCover(slide, getAssetPath("images", data.image), {
      x: 0,
      y: 0,
      w: IMG_W,
      h: 7.5,
    });
  }

  slide.addText(content.title, {
    x: TEXT_X,
    y: 0.7,
    w: TEXT_W,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: TEXT_X,
      y: 1.55,
      w: TEXT_W,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  let nextY = 2.3;

  if (content.body) {
    slide.addText(content.body, {
      x: TEXT_X,
      y: nextY,
      w: TEXT_W,
      h: 2.0,
      fontSize: 14,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
    nextY += 2.2;
  }

  if (content.steps && content.steps.length > 0) {
    renderInlineSteps(slide, content.steps, TEXT_X, nextY, TEXT_W);
  } else if (content.options && content.options.length > 0) {
    renderInlineOptions(slide, content.options, TEXT_X, nextY, TEXT_W);
  } else if (content.metrics && content.metrics.length > 0) {
    renderInlineMetrics(slide, content.metrics, TEXT_X, nextY, TEXT_W);
  }

  addFooter(slide, slideNumber);
}

export function renderInfoLayout6b(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  if (data.image) {
    addImageCover(slide, getAssetPath("images", data.image), {
      x: 0,
      y: 0,
      w: IMG_W,
      h: 7.5,
    });
  }

  slide.addText(content.title, {
    x: TEXT_X,
    y: 0.7,
    w: TEXT_W,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  if (content.body) {
    const parts = content.body.split("\n\n");
    const col1 = parts[0] ?? "";
    const col2 = parts.slice(1).join("\n\n");
    const colW = 2.8;

    slide.addText(col1, {
      x: TEXT_X,
      y: 1.8,
      w: colW,
      h: 4.8,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });

    slide.addText(col2, {
      x: TEXT_X + colW + 0.4,
      y: 1.8,
      w: colW,
      h: 4.8,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}

export function renderInfoLayout2a(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: MARGIN,
    y: 0.7,
    w: FULL_W,
    h: 0.8,
    fontSize: 26,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: MARGIN,
      y: 1.55,
      w: FULL_W,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  const options = content.options ?? [];
  const colCount = Math.min(options.length, 3);
  const colWidth = 3.6;
  const startX = MARGIN;
  const startY = 2.4;
  const gap = 0.4;

  for (let i = 0; i < colCount; i++) {
    const x = startX + i * (colWidth + gap);

    if (i > 0) {
      addSeparatorLine(slide, x - gap / 2, startY, 4.0);
    }

    if (data.icons && data.icons[i]) {
      addIcon(slide, data.icons[i], { x: x + 0.1, y: startY, size: 0.6 });
    }

    slide.addText(options[i].title, {
      x,
      y: startY + 0.8,
      w: colWidth,
      h: 0.5,
      fontSize: 16,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.erniBlue,
      bold: true,
    });

    slide.addText(options[i].description, {
      x,
      y: startY + 1.4,
      w: colWidth,
      h: 2.8,
      fontSize: 12,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      valign: "top",
    });
  }

  addFooter(slide, slideNumber);
}
