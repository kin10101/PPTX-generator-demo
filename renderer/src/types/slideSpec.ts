import { z } from "zod";

const SlideContentSchema = z.object({
  title: z.string(),
  subtitle: z.string().optional(),
  body: z.string().optional(),
  options: z
    .array(z.object({ title: z.string(), description: z.string() }))
    .optional(),
  steps: z
    .array(
      z.object({
        number: z.string().optional(),
        title: z.string(),
        description: z.string(),
      })
    )
    .optional(),
  metrics: z
    .array(z.object({ value: z.string(), label: z.string() }))
    .optional(),
  footnote: z.string().optional(),
});

const SlideSchema = z.object({
  slideIndex: z.number(),
  layoutName: z.string(),
  image: z.string().optional(),
  icons: z.array(z.string()).optional(),
  content: SlideContentSchema,
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
export type SlideContent = z.infer<typeof SlideContentSchema>;
