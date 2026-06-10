import { z } from "zod";

const TextElementSchema = z.object({
  type: z.literal("text"),
  content: z.string(),
  x: z.number(),
  y: z.number(),
  w: z.number(),
  h: z.number(),
  fontSize: z.number().optional(),
  fontFace: z.string().optional(),
  color: z.string().optional(),
  bold: z.boolean().optional(),
  italic: z.boolean().optional(),
  align: z.enum(["left", "center", "right"]).optional(),
  valign: z.enum(["top", "middle", "bottom"]).optional(),
  autoFit: z.boolean().optional(),
  lineSpacing: z.number().optional(),
});

const ImageElementSchema = z.object({
  type: z.literal("image"),
  src: z.string(),
  x: z.number(),
  y: z.number(),
  w: z.number(),
  h: z.number(),
  sizing: z
    .object({
      type: z.enum(["cover", "contain"]),
      w: z.number(),
      h: z.number(),
    })
    .optional(),
});

const ShapeElementSchema = z.object({
  type: z.literal("shape"),
  shape: z.enum(["rect", "ellipse", "line"]),
  x: z.number(),
  y: z.number(),
  w: z.number(),
  h: z.number(),
  fill: z.string().optional(),
  line: z.object({ color: z.string(), width: z.number() }).optional(),
  rectRadius: z.number().optional(),
});

const IconElementSchema = z.object({
  type: z.literal("icon"),
  src: z.string(),
  x: z.number(),
  y: z.number(),
  w: z.number(),
  h: z.number(),
});

const SlideElementSchema = z.discriminatedUnion("type", [
  TextElementSchema,
  ImageElementSchema,
  ShapeElementSchema,
  IconElementSchema,
]);

const SlideSchema = z.object({
  slideIndex: z.number(),
  background: z
    .object({
      color: z.string().optional(),
      image: z.string().optional(),
    })
    .optional(),
  footer: z.boolean().optional().default(true),
  elements: z.array(SlideElementSchema),
});

export const SlideSpecSchema = z.object({
  metadata: z.object({
    title: z.string(),
    output: z.string(),
  }),
  slides: z.array(SlideSchema),
});

export type SlideSpec = z.infer<typeof SlideSpecSchema>;
export type SlideData = z.infer<typeof SlideSchema>;
export type SlideElement = z.infer<typeof SlideElementSchema>;
export type TextElement = z.infer<typeof TextElementSchema>;
export type ImageElement = z.infer<typeof ImageElementSchema>;
export type ShapeElement = z.infer<typeof ShapeElementSchema>;
export type IconElement = z.infer<typeof IconElementSchema>;
