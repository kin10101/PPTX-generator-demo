#!/usr/bin/env python3
"""Validate that a generated PPTX uses only bundled template, icon, and image media.

Run from anywhere:
    python scripts/validate_deck_assets.py path/to/deck.pptx

The allowlist is built from:
- assets/templates/erni_master_template.pptx media
- assets/images/*
- assets/icons/template-media/*
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

MEDIA_PREFIX = "ppt/media/"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp", ".emf", ".wmf"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add_file_hashes(root: Path, allowed: dict[str, list[str]]) -> None:
    if not root.exists():
        return
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.suffix.lower() in IMAGE_EXTS:
            digest = sha256_bytes(path.read_bytes())
            allowed.setdefault(digest, []).append(str(path.relative_to(root.parent.parent)))


def add_template_media_hashes(template_path: Path, allowed: dict[str, list[str]]) -> None:
    if not template_path.exists():
        return
    with zipfile.ZipFile(template_path) as zf:
        for name in zf.namelist():
            if name.startswith(MEDIA_PREFIX):
                data = zf.read(name)
                digest = sha256_bytes(data)
                allowed.setdefault(digest, []).append(f"{template_path.name}:{name}")


def build_allowlist(skill_root: Path) -> dict[str, list[str]]:
    allowed: dict[str, list[str]] = {}
    add_template_media_hashes(skill_root / "assets" / "templates" / "erni_master_template.pptx", allowed)
    add_file_hashes(skill_root / "assets" / "images", allowed)
    add_file_hashes(skill_root / "assets" / "icons", allowed)
    return allowed


def find_deck_media(deck_path: Path) -> list[tuple[str, str, int]]:
    with zipfile.ZipFile(deck_path) as zf:
        rows = []
        for name in sorted(zf.namelist()):
            if name.startswith(MEDIA_PREFIX):
                data = zf.read(name)
                rows.append((name, sha256_bytes(data), len(data)))
        return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="validate bundled-media-only use in a generated erni pptx")
    parser.add_argument("deck", type=Path, help="pptx file to validate")
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--list", action="store_true", help="print every deck media item and its allowlist match")
    args = parser.parse_args()

    deck_path = args.deck.resolve()
    if not deck_path.exists():
        print(f"error: deck not found: {deck_path}", file=sys.stderr)
        return 2
    if deck_path.suffix.lower() != ".pptx":
        print(f"error: expected a .pptx file: {deck_path}", file=sys.stderr)
        return 2

    allowed = build_allowlist(args.skill_root.resolve())
    media = find_deck_media(deck_path)
    unauthorized = []

    for name, digest, size in media:
        matches = allowed.get(digest, [])
        if args.list:
            label = ", ".join(matches[:3]) if matches else "unauthorized"
            print(f"{name}\t{size}\t{label}")
        if not matches:
            unauthorized.append((name, size, digest))

    if unauthorized:
        print("unauthorized ppt/media assets found:", file=sys.stderr)
        for name, size, digest in unauthorized:
            print(f"- {name} ({size} bytes, sha256={digest[:16]}...)", file=sys.stderr)
        print("replace these with assets/images/*, assets/icons/template-media/*, or template-native graphics.", file=sys.stderr)
        return 1

    print(f"ok: {len(media)} ppt/media assets are from the bundled template/images/icons allowlist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
