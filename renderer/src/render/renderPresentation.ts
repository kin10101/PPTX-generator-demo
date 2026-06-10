import PptxGenJS from "pptxgenjs";
import { SlideSpec } from "../types/slideSpec.js";
import { renderSlide } from "../render/index.js";
import path from "path";
import { mkdirSync } from "fs";

export async function renderPresentation(spec: SlideSpec): Promise<string> {
  // @ts-expect-error PptxGenJS default export typing with NodeNext
  const pptx = new PptxGenJS();

  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "ERNI PPTX Generator";
  pptx.title = spec.metadata.title;

  for (let i = 0; i < spec.slides.length; i++) {
    renderSlide(pptx, spec.slides[i], i + 1);
  }

  const outputPath = path.resolve(spec.metadata.output);
  mkdirSync(path.dirname(outputPath), { recursive: true });

  await pptx.writeFile({ fileName: outputPath });
  return outputPath;
}
