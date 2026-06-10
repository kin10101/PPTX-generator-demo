import { createHash } from "crypto";
import { readdirSync, readFileSync, statSync, existsSync } from "fs";
import path from "path";
import AdmZip from "adm-zip";

const MEDIA_PREFIX = "ppt/media/";
const IMAGE_EXTS = new Set([
  ".jpg",
  ".jpeg",
  ".png",
  ".svg",
  ".gif",
  ".webp",
  ".emf",
  ".wmf",
]);

function sha256(data: Buffer): string {
  return createHash("sha256").update(data).digest("hex");
}

function addFileHashes(
  root: string,
  allowed: Map<string, string[]>
): void {
  if (!existsSync(root)) return;

  function walk(dir: string) {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (IMAGE_EXTS.has(path.extname(entry.name).toLowerCase())) {
        const digest = sha256(readFileSync(full));
        const rel = path.relative(path.resolve(root, "../.."), full);
        if (!allowed.has(digest)) allowed.set(digest, []);
        allowed.get(digest)!.push(rel);
      }
    }
  }

  walk(root);
}

function addTemplateMediaHashes(
  templatePath: string,
  allowed: Map<string, string[]>
): void {
  if (!existsSync(templatePath)) return;

  const zip = new AdmZip(templatePath);
  for (const entry of zip.getEntries()) {
    if (entry.entryName.startsWith(MEDIA_PREFIX)) {
      const data = entry.getData();
      const digest = sha256(data);
      const label = `${path.basename(templatePath)}:${entry.entryName}`;
      if (!allowed.has(digest)) allowed.set(digest, []);
      allowed.get(digest)!.push(label);
    }
  }
}

function buildAllowlist(skillRoot: string): Map<string, string[]> {
  const allowed = new Map<string, string[]>();
  addTemplateMediaHashes(
    path.join(skillRoot, "assets/templates/erni_master_template.pptx"),
    allowed
  );
  addFileHashes(path.join(skillRoot, "assets/images"), allowed);
  addFileHashes(path.join(skillRoot, "assets/icons"), allowed);
  return allowed;
}

export interface ValidationResult {
  ok: boolean;
  total: number;
  unauthorized: Array<{ name: string; size: number; sha256: string }>;
}

export function validateDeckAssets(
  deckPath: string,
  skillRoot?: string
): ValidationResult {
  const root =
    skillRoot ??
    path.resolve(
      import.meta.dirname,
      "../../..",
      "skill/erni-powerpoint-builder"
    );

  const allowed = buildAllowlist(root);
  const zip = new AdmZip(deckPath);
  const unauthorized: ValidationResult["unauthorized"] = [];
  let total = 0;

  for (const entry of zip.getEntries()) {
    if (entry.entryName.startsWith(MEDIA_PREFIX)) {
      total++;
      const data = entry.getData();
      const digest = sha256(data);
      if (!allowed.has(digest)) {
        unauthorized.push({
          name: entry.entryName,
          size: data.length,
          sha256: digest,
        });
      }
    }
  }

  return { ok: unauthorized.length === 0, total, unauthorized };
}
