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
      const hex = data.background.color.replace(/^#/, "");
      slide.background = { color: hex.length === 8 ? hex.slice(0, 6) : hex };
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
