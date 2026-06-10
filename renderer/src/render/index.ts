import { Pptx } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import { renderSlideElements } from "./engine.js";
import { addFooter, getAssetPath } from "./helpers.js";

export function renderSlide(
  pptx: Pptx,
  data: SlideData,
  slideNumber: number
): void {
  const slide = pptx.addSlide();

  if (data.background) {
    if (data.background.color) {
      slide.background = { color: data.background.color };
    }
    if (data.background.image) {
      const imgPath = getAssetPath("images", data.background.image);
      slide.background = { path: imgPath };
    }
  }

  renderSlideElements(slide, data.elements);

  if (data.footer !== false) {
    addFooter(slide, slideNumber);
  }
}
