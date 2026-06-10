import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { addFooter, addImageCover, getAssetPath } from "./helpers.js";

export function renderCoverLayout1(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  if (data.image) {
    addImageCover(slide, getAssetPath("images", data.image), {
      x: 6.67,
      y: 0,
      w: 6.66,
      h: 7.5,
    });
  }

  slide.addText(content.title, {
    x: 0.8,
    y: 2.4,
    w: 5.5,
    h: 1.8,
    fontSize: 36,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
    valign: "bottom",
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: 0.8,
      y: 4.4,
      w: 5.5,
      h: 1.0,
      fontSize: 18,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
    });
  }

  addFooter(slide, slideNumber);
}

export function renderCoverLayout2(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: 1.0,
    y: 2.5,
    w: 11.33,
    h: 1.6,
    fontSize: 40,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
    align: "center",
    valign: "middle",
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: 2.0,
      y: 4.2,
      w: 9.33,
      h: 1.0,
      fontSize: 20,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "center",
    });
  }

  addFooter(slide, slideNumber);
}

export function renderCoverLayout3(
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
): void {
  const { content } = data;

  slide.addText(content.title, {
    x: 6.0,
    y: 2.5,
    w: 6.5,
    h: 1.6,
    fontSize: 36,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.erniBlue,
    bold: true,
    align: "right",
  });

  if (content.subtitle) {
    slide.addText(content.subtitle, {
      x: 6.0,
      y: 4.2,
      w: 6.5,
      h: 1.0,
      fontSize: 18,
      fontFace: ERNI_THEME.font,
      color: ERNI_THEME.colors.darkGray,
      align: "right",
    });
  }

  addFooter(slide, slideNumber);
}
