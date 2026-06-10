import { ERNI_THEME } from "../config/theme.js";
import { Pptx, PptxSlide } from "../types/pptx.js";
import path from "path";

const SKILL_ROOT = path.resolve(
  import.meta.dirname,
  "../../..",
  "skill/erni-powerpoint-builder"
);

export function getAssetPath(
  category: "images" | "icons/template-media",
  filename: string
): string {
  return path.join(SKILL_ROOT, "assets", category, filename);
}

export function addFooter(slide: PptxSlide, slideNumber: number): void {
  const { footer } = ERNI_THEME;

  slide.addText(footer.text, {
    x: footer.position.x,
    y: footer.position.y,
    w: 2,
    h: 0.25,
    fontSize: footer.fontSize,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.lightGray,
    bold: false,
  });

  slide.addText(String(slideNumber), {
    x: footer.slideNumberPosition.x,
    y: footer.slideNumberPosition.y,
    w: 0.5,
    h: 0.25,
    fontSize: footer.fontSize,
    fontFace: ERNI_THEME.font,
    color: ERNI_THEME.colors.lightGray,
    align: "right",
  });
}

export function addImageCover(
  slide: PptxSlide,
  imagePath: string,
  bounds: { x: number; y: number; w: number; h: number }
): void {
  slide.addImage({
    path: imagePath,
    ...bounds,
    sizing: { type: "cover", w: bounds.w, h: bounds.h },
  });
}

export function addIcon(
  slide: PptxSlide,
  iconFile: string,
  position: { x: number; y: number; size?: number }
): void {
  const size = position.size ?? 0.5;
  slide.addImage({
    path: getAssetPath("icons/template-media", iconFile),
    x: position.x,
    y: position.y,
    w: size,
    h: size,
  });
}

export function addSeparatorLine(
  slide: PptxSlide,
  x: number,
  y: number,
  height: number
): void {
  slide.addShape("line", {
    x,
    y,
    w: 0,
    h: height,
    line: { color: ERNI_THEME.colors.erniBlue, width: 1 },
  });
}
