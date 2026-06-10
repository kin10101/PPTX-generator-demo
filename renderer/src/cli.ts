import { Command } from "commander";
import { readFileSync } from "fs";
import { SlideSpecSchema } from "./types/slideSpec.js";
import { renderPresentation } from "./render/renderPresentation.js";
import { validateDeckAssets } from "./validation/validateDeckAssets.js";

const program = new Command();

program
  .name("erni-pptx-renderer")
  .description("Deterministic PPTX renderer for ERNI presentations")
  .version("0.1.0");

program
  .command("render")
  .description("Render a slide specification JSON into a .pptx file")
  .requiredOption("-i, --input <path>", "Path to slide spec JSON file")
  .option("-o, --output <path>", "Override output path from spec")
  .action(async (opts) => {
    const raw = readFileSync(opts.input, "utf-8");
    const json = JSON.parse(raw);

    if (opts.output) {
      json.metadata = { ...json.metadata, output: opts.output };
    }

    const parsed = SlideSpecSchema.safeParse(json);
    if (!parsed.success) {
      console.error("Invalid slide spec:");
      for (const issue of parsed.error.issues) {
        console.error(`  ${issue.path.join(".")}: ${issue.message}`);
      }
      process.exit(1);
    }

    try {
      const outputPath = await renderPresentation(parsed.data);
      const validation = validateDeckAssets(outputPath);

      if (validation.ok) {
        console.log(`OK: ${outputPath} (${validation.total} media assets validated)`);
      } else {
        console.log(`WARN: ${outputPath} generated with ${validation.unauthorized.length} unauthorized assets:`);
        for (const item of validation.unauthorized) {
          console.log(`  - ${item.name} (${item.size} bytes)`);
        }
      }
    } catch (err: any) {
      console.error(`Render failed: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command("validate")
  .description("Validate that a .pptx uses only approved media assets")
  .argument("<deck>", "Path to .pptx file")
  .option("--skill-root <path>", "Override skill root directory")
  .option("--list", "Print each media item and its match status")
  .action((deck, opts) => {
    try {
      const result = validateDeckAssets(deck, opts.skillRoot);

      if (opts.list) {
        console.log(`Total media entries: ${result.total}`);
        if (result.unauthorized.length > 0) {
          console.log("\nUnauthorized:");
          for (const item of result.unauthorized) {
            console.log(`  ${item.name} (${item.size} bytes, sha256=${item.sha256.slice(0, 16)}...)`);
          }
        }
      }

      if (result.ok) {
        console.log(`OK: ${result.total} media assets are from the bundled allowlist.`);
      } else {
        console.error(`FAIL: ${result.unauthorized.length} unauthorized media assets found.`);
        if (!opts.list) {
          for (const item of result.unauthorized) {
            console.error(`  - ${item.name} (${item.size} bytes)`);
          }
        }
        process.exit(1);
      }
    } catch (err: any) {
      console.error(`Validation failed: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();
