#!/usr/bin/env python3
"""Aggregates markdownlint, cspell, vale, lychee, and front-matter results
into a single ranked report of issues per file under docs/."""
import json
import os
import urllib.parse
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE)


def norm(path):
    """Normalize a path to be relative to the repo root, POSIX separators."""
    path = path.replace('\\', '/')
    if path.startswith(REPO_ROOT):
        path = os.path.relpath(path, REPO_ROOT)
    return path


counts = defaultdict(lambda: defaultdict(int))
details = defaultdict(lambda: defaultdict(list))
all_files = set()


def walk_docs():
    docs_dir = os.path.join(REPO_ROOT, 'docs')
    for root, _dirs, files in os.walk(docs_dir):
        for name in files:
            if name.endswith('.md') or name.endswith('.mdx'):
                all_files.add(norm(os.path.join(root, name)))


walk_docs()


def add(file, category, note=None, n=1):
    file = norm(file)
    all_files.add(file)
    counts[file][category] += n
    if note:
        details[file][category].append(note)


# 1. markdownlint-cli2 results
with open(os.path.join(BASE, 'markdownlint-results.json')) as f:
    for item in json.load(f):
        rule = '/'.join(item['ruleNames'][:2])
        add(item['fileName'], 'markdown_syntax', f"{rule}: {item['ruleDescription']} (line {item['lineNumber']})")

# 2. cspell results
with open(os.path.join(BASE, 'cspell-results.json')) as f:
    cspell_data = json.load(f)
    for issue in cspell_data['issues']:
        p = urllib.parse.unquote(urllib.parse.urlparse(issue['uri']).path)
        add(p, 'spelling', f"'{issue['text']}' (line {issue['row']})")

# 3. vale results (grammar/style/prose)
with open(os.path.join(BASE, 'vale-results.json')) as f:
    vale_data = json.load(f)
    for file, issues in vale_data.items():
        for issue in issues:
            add(file, 'grammar_style', f"{issue['Check']}: {issue['Message']} (line {issue['Line']})")

# 4. lychee results (broken links)
with open(os.path.join(BASE, 'lychee-results.json')) as f:
    lychee_data = json.load(f)
    for file, issues in lychee_data.get('error_map', {}).items():
        for issue in issues:
            add(file, 'broken_links', f"{issue['url']}: {issue['status']['text']} (line {issue['span']['line']})")

# 5. front-matter/metadata results
with open(os.path.join(BASE, 'frontmatter-results.json')) as f:
    fm_data = json.load(f)
    for item in fm_data:
        file = os.path.join('docs', item['file'])
        for issue in item['issues']:
            add(file, 'metadata', issue)

CATEGORIES = ['markdown_syntax', 'spelling', 'grammar_style', 'broken_links', 'metadata']

rows = []
for file in all_files:
    total = sum(counts[file].values())
    rows.append({
        'file': file,
        'name': os.path.basename(file),
        'total': total,
        'by_category': {c: counts[file].get(c, 0) for c in CATEGORIES},
        'details': details[file],
    })

rows.sort(key=lambda r: (r['total'], r['file']))
for i, r in enumerate(rows, start=1):
    r['rank'] = i

with open(os.path.join(BASE, 'aggregated-results.json'), 'w') as f:
    json.dump(rows, f, indent=2)

print(f"Aggregated {len(rows)} files. Report data written to aggregated-results.json")
print(f"Total issues across corpus: {sum(r['total'] for r in rows)}")
