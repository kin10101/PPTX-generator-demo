import { PptxSlide } from "../types/pptx.js";
import {
  SlideElement,
  TextElement,
  ImageElement,
  ShapeElement,
  IconElement,
} from "../types/slideSpec.js";
import { getAssetPath } from "./helpers.js";

export function renderSlideElements(
  slide: PptxSlide,
  elements: SlideElement[]
): void {
  for (const el of elements) {
    switch (el.type) {
      case "text":
        renderText(slide, el);
        break;
      case "image":
        renderImage(slide, el);
        break;
      case "shape":
        renderShape(slide, el);
        break;
      case "icon":
        renderIcon(slide, el);
        break;
    }
  }
}

function toRgb(hex: string | undefined): string | undefined {
  if (!hex) return undefined;
  const h = hex.replace(/^#/, "");
  return h.length === 8 ? h.slice(0, 6) : h;
}

function renderText(slide: PptxSlide, el: TextElement): void {
  slide.addText(el.content, {
    x: el.x,
    y: el.y,
    w: el.w,
    h: el.h,
    fontSize: el.fontSize,
    fontFace: el.fontFace,
    color: toRgb(el.color),
    bold: el.bold,
    italic: el.italic,
    align: el.align,
    valign: el.valign,
    autoFit: el.autoFit,
    lineSpacingMultiple: el.lineSpacing,
  });
}

function renderImage(slide: PptxSlide, el: ImageElement): void {
  const resolvedPath = resolveAssetSrc(el.src);
  slide.addImage({
    path: resolvedPath,
    x: el.x,
    y: el.y,
    w: el.w,
    h: el.h,
    sizing: el.sizing,
  });
}

function renderShape(slide: PptxSlide, el: ShapeElement): void {
  slide.addShape(el.shape, {
    x: el.x,
    y: el.y,
    w: el.w,
    h: el.h,
    fill: el.fill ? { color: toRgb(el.fill)! } : undefined,
    line: el.line ? { ...el.line, color: toRgb(el.line.color)! } : undefined,
    rectRadius: el.rectRadius,
  });
}

function renderIcon(slide: PptxSlide, el: IconElement): void {
  const resolvedPath = resolveAssetSrc(el.src);
  slide.addImage({
    path: resolvedPath,
    x: el.x,
    y: el.y,
    w: el.w,
    h: el.h,
  });
}

function resolveAssetSrc(src: string): string {
  if (src.startsWith("images/")) {
    return getAssetPath("images", src.slice("images/".length));
  }
  if (src.startsWith("icons/template-media/")) {
    return getAssetPath(
      "icons/template-media",
      src.slice("icons/template-media/".length)
    );
  }
  return getAssetPath("images", src);
}
