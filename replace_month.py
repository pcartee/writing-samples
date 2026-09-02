#!/usr/bin/env python3
"""
replace_month.py

Replace the numeric month (MM) with the full month name in date tokens of
the form:

    *· MM/DD/YYYY ·*

across all Markdown (`.md`) and MDX (`.mdx`) files under the `docs/`
directory, leaving every other reference (e.g. the `date:` field in YAML
frontmatter) untouched.

The rewrite is idempotent: months already written as names (e.g.
`*· May/01/2025 ·*`) are left unchanged, so the script is safe to run more
than once.

Excluded directories (relative to `docs/`, case-insensitive):
    include-shared
    ita/include

Usage:
    # Preview changes without writing any files
    python replace_month.py --dry-run

    # Apply changes
    python replace_month.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCS_DIR = Path(__file__).resolve().parent / "docs"

EXTENSIONS = {".md", ".mdx"}

# Directory prefixes (relative to DOCS_DIR, case-insensitive) to skip.
EXCLUDED_PREFIXES = (
    "include-shared",
    "ita/include",
)

# Full month names, keyed by 1-based month number.
MONTHS = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}

# Matches `*· MM/DD/YYYY ·*`, capturing the `*· ` prefix, the two-digit month,
# and the `/DD/YYYY ·*` suffix so only the month number is rewritten.
DATE_TOKEN_RE = re.compile(r"(\*· )(\d{2})(/\d{2}/\d{4} ·\*)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_excluded(rel_path: Path) -> bool:
    """Return True if a path (relative to DOCS_DIR) falls under an excluded dir."""
    parts = [p.lower() for p in rel_path.parts]
    for prefix in EXCLUDED_PREFIXES:
        pref = prefix.split("/")
        if parts[: len(pref)] == pref:
            return True
    return False


def _replace_months(text: str) -> tuple[str, int]:
    """Rewrite the numeric month in each `*· MM/DD/YYYY ·*` token.

    Returns (new_text, replacements). Tokens whose month isn't 01-12 (or is
    already a name) are left unchanged.
    """
    count = 0

    def _sub(match: re.Match[str]) -> str:
        nonlocal count
        name = MONTHS.get(int(match.group(2)))
        if name is None:
            return match.group(0)
        count += 1
        return f"{match.group(1)}{name}{match.group(3)}"

    return DATE_TOKEN_RE.sub(_sub, text), count


def _iter_target_files(base: Path):
    """Yield candidate files under base, skipping excluded directories."""
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in EXTENSIONS:
            continue
        if _is_excluded(path.relative_to(base)):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace numeric months with names in `*· MM/DD/YYYY ·*` tokens.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without writing any files"
    )
    args = parser.parse_args()

    base = DOCS_DIR
    if not base.is_dir():
        print(f"error: docs directory not found at {base}", file=sys.stderr)
        return 1

    files_changed = 0
    total_replacements = 0

    for path in sorted(_iter_target_files(base)):
        rel = path.relative_to(base)

        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            print(f"  warn: skipped {rel} (not UTF-8: {exc})", file=sys.stderr)
            continue

        new_text, count = _replace_months(text)
        if count == 0:
            continue

        total_replacements += count
        if args.dry_run:
            print(f"  [dry-run] {rel}: {count} replacement(s)")
        else:
            path.write_bytes(new_text.encode("utf-8"))
        files_changed += 1

    print(f"\n{'Dry-run complete (no files modified)' if args.dry_run else 'Done'}.")
    print(f"Files changed:  {files_changed}")
    print(f"Replacements:   {total_replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
