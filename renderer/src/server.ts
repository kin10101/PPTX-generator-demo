import express from "express";
import { SlideSpecSchema } from "./types/slideSpec.js";
import { renderPresentation } from "./render/renderPresentation.js";
import { validateDeckAssets } from "./validation/validateDeckAssets.js";

const app = express();
app.use(express.json({ limit: "10mb" }));

app.post("/render", async (req, res) => {
  const parsed = SlideSpecSchema.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json({ error: "Invalid slide spec", details: parsed.error.issues });
    return;
  }

  try {
    const outputPath = await renderPresentation(parsed.data);
    const validation = validateDeckAssets(outputPath);
    res.json({ outputPath, validation });
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/validate", async (req, res) => {
  const { deckPath, skillRoot } = req.body;
  if (!deckPath || typeof deckPath !== "string") {
    res.status(400).json({ error: "deckPath is required" });
    return;
  }

  try {
    const result = validateDeckAssets(deckPath, skillRoot);
    res.json(result);
  } catch (err: any) {
    res.status(500).json({ error: err.message });
  }
});

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

const port = parseInt(process.env.PORT ?? "3001", 10);
app.listen(port, () => {
  console.log(`ERNI PPTX Renderer listening on port ${port}`);
});
