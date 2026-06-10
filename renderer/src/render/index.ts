import { Pptx, PptxSlide } from "../types/pptx.js";
import { SlideData } from "../types/slideSpec.js";
import {
  renderCoverLayout1,
  renderCoverLayout2,
  renderCoverLayout3,
} from "./cover.js";
import { renderSectionLayout1 } from "./section.js";
import {
  renderInfoLayout5a,
  renderInfoLayout5b,
  renderInfoLayout6a,
  renderInfoLayout6b,
  renderInfoLayout2a,
} from "./info.js";
import { renderFlowLayout3b } from "./flow.js";
import { renderChartLayout2a } from "./chart.js";
import { renderContainersLayout } from "./containers.js";
import { renderPeopleLayout1 } from "./people.js";
import {
  renderBackCover1,
  renderBackCover2,
  renderBackCover3,
} from "./backCover.js";

type SlideRenderer = (
  pptx: Pptx,
  slide: PptxSlide,
  data: SlideData,
  slideNumber: number
) => void;

const LAYOUT_MAP: Array<{ match: string; renderer: SlideRenderer }> = [
  { match: "Cover Layout 1", renderer: renderCoverLayout1 },
  { match: "Cover Layout 2", renderer: renderCoverLayout2 },
  { match: "Cover Layout 3", renderer: renderCoverLayout3 },
  { match: "Section Layout 1", renderer: renderSectionLayout1 },
  { match: "Info Layout 5a", renderer: renderInfoLayout5a },
  { match: "Info Layout 5b", renderer: renderInfoLayout5b },
  { match: "Info Layout Image and Text 6a", renderer: renderInfoLayout6a },
  { match: "Info Layout Image and Text 6b", renderer: renderInfoLayout6b },
  { match: "Info Layout 6a", renderer: renderInfoLayout6a },
  { match: "Info Layout 6b", renderer: renderInfoLayout6b },
  { match: "Info Layout 2a", renderer: renderInfoLayout2a },
  { match: "Flow Layout 3b", renderer: renderFlowLayout3b },
  { match: "Chart Layout 2a", renderer: renderChartLayout2a },
  { match: "Containers Layout", renderer: renderContainersLayout },
  { match: "People Layout 1", renderer: renderPeopleLayout1 },
  { match: "Back Cover 1", renderer: renderBackCover1 },
  { match: "1_Back Cover 1", renderer: renderBackCover1 },
  { match: "Back Cover 2", renderer: renderBackCover2 },
  { match: "Back Cover 3", renderer: renderBackCover3 },
];

export function resolveRenderer(layoutName: string): SlideRenderer | null {
  const normalized = layoutName.trim().toLowerCase();
  for (const entry of LAYOUT_MAP) {
    if (normalized.includes(entry.match.toLowerCase())) {
      return entry.renderer;
    }
  }
  return null;
}

export function renderSlide(
  pptx: Pptx,
  data: SlideData,
  slideNumber: number
): void {
  const renderer = resolveRenderer(data.layoutName);
  const slide = pptx.addSlide();

  if (renderer) {
    renderer(pptx, slide, data, slideNumber);
  } else {
    renderInfoLayout5a(pptx, slide, data, slideNumber);
  }
}
