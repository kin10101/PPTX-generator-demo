import PptxGenJS from "pptxgenjs";

// PptxGenJS types don't export cleanly under NodeNext module resolution.
// Use `any` for the slide type — runtime behavior is correct.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Pptx = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type PptxSlide = any;

export { PptxGenJS };
