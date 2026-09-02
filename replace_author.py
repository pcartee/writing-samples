#!/usr/bin/env python3
"""Replace the value of every ``author:`` frontmatter field with a single name.

By default this walks ``/docs`` recursively, finds every ``.md`` and ``.mdx``
file, and rewrites the value that follows ``author:`` in the YAML frontmatter
to ``pcartee`` -- e.g.::

    author: Paul Cartee          ->  author: pcartee
    author: carteepaul, mkwilbux ->  author: pcartee

Notes / guarantees:
* Only the frontmatter block (between the opening and closing ``---``) is
  touched, so prose that merely contains the word "author" or the product name
  "Trust Authority" is never modified.
* Matching is limited to an ``author:`` key at the start of a line (optional
  leading spaces/tabs), so values with commas, spaces, etc. are fully replaced.
* File encoding (UTF-8), BOM, line endings, and all other keys are preserved.
* Files are rewritten only when a change actually occurs, so the script is
  idempotent -- re-running it is safe and a no-op.

Usage:
    python3 replace_author.py                 # real run against /docs
    python3 replace_author.py --dry-run       # preview changes, write nothing
    python3 replace_author.py --value pcartee # use a different replacement
    python3 replace_author.py /other/docs     # point at another directory
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_DOCS_DIR = "/Users/pcartee/github/writing-samples/docs"
DEFAULT_VALUE = "pcartee"
EXTENSIONS = (".md", ".mdx")

# ``author:`` (optionally indented) at the start of a line, followed by the
# rest of that line (any characters except a newline). Stopping at the first
# newline preserves an existing ``\r`` for CRLF files.
AUTHOR_RE = re.compile(r"(?m)^([ \t]*author:)[^\r\n]*")


@dataclass
class Result:
    """Aggregated outcome of the run plus a per-file report."""

    scanned: int = 0
    changed: int = 0
    errors: int = 0
    details: list[str] = field(default_factory=list)


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return ``(frontmatter, rest)`` if the file starts with a YAML block.

    ``frontmatter`` runs from the opening ``---`` line through just before the
    closing delimiter, and ``rest`` starts at the closing delimiter, so that
    ``frontmatter + rest`` reconstructs the original text exactly. Returns
    ``(None, text)`` when no frontmatter is present.
    """
    # Allow an optional UTF-8 BOM and leading blank lines before the delimiter.
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            # frontmatter includes the opening delimiter (lines[0]) through just
            # before the closing delimiter; rest starts at the closing line. The
            # author regex never matches a "---" line, so keeping the opening
            # delimiter in the region we scan is safe and lossless.
            return "".join(lines[:i]), "".join(lines[i:])
    return None, text  # no closing delimiter -> treat as having no frontmatter


def process_file(path: Path, value: str, write: bool = True) -> tuple[bool, list[str]]:
    """Rewrite ``author:`` value(s) in one file.

    Returns ``(changed, log)`` where ``changed`` is ``True`` only if the file
    content actually differs from what it was before. Pass ``write=False`` for a
    dry run: the change is computed and reported but the file is left untouched.
    """
    original = path.read_text(encoding="utf-8", newline="")
    fm, rest = split_frontmatter(original)
    if fm is None:
        return False, []

    new_fm, n = AUTHOR_RE.subn(lambda m: m.group(1) + " " + value, fm)
    if n == 0:
        return False, []

    new_text = new_fm + rest
    if new_text == original:
        return False, []  # value was already correct -> idempotent no-op

    old_value = AUTHOR_RE.search(fm)
    if write:
        path.write_text(new_text, encoding="utf-8", newline="")
    log = [f"  {path}: {old_value.group(0).strip()!r} -> {value!r}"]
    return True, log


def collect_files(docs_dir: Path) -> list[Path]:
    return sorted(
        p for ext in EXTENSIONS
        for p in docs_dir.rglob(f"*{ext}")
        if p.is_file()
    )


def run(docs_dir: Path, value: str, dry_run: bool) -> Result:
    result = Result()
    if not docs_dir.is_dir():
        result.errors += 1
        result.details.append(f"ERROR: directory not found: {docs_dir}")
        return result

    files = collect_files(docs_dir)
    result.scanned = len(files)
    if not files:
        result.details.append(f"No {', '.join(EXTENSIONS)} files found under {docs_dir}")
        return result

    for path in files:
        try:
            changed, log = process_file(path, value, write=not dry_run)
        except Exception as exc:  # keep going on a per-file error
            result.errors += 1
            result.details.append(f"ERROR: {path}: {exc}")
            continue
        if changed:
            result.changed += 1
            result.details.append(f"{'[dry-run] ' if dry_run else ''}updated {path}")
            result.details.extend(log)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace the value of every 'author:' frontmatter field in .md/.mdx files.",
    )
    parser.add_argument(
        "docs_dir",
        nargs="?",
        default=DEFAULT_DOCS_DIR,
        help=f"Directory to scan recursively (default: {DEFAULT_DOCS_DIR})",
    )
    parser.add_argument(
        "--value",
        default=DEFAULT_VALUE,
        help=f"Replacement string for the author value (default: {DEFAULT_VALUE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing any files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = run(Path(args.docs_dir), args.value, args.dry_run)

    verb = "would update" if args.dry_run else "updated"
    print(f"Scanned : {result.scanned} file(s)")
    print(f"{verb.capitalize()} : {result.changed} file(s)")
    if result.errors:
        print(f"Errors  : {result.errors}")
    for line in result.details:
        print(line)
    return 0 if result.errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
