#!/usr/bin/env node
// Checks docs/ front matter against this repo's schema and flags issues per file.
// Output: JSON lines of {file, issues: [string, ...]}
'use strict';
const fs = require('fs');
const path = require('path');

const DOCS_ROOT = path.resolve(__dirname, '..', 'docs');
const REQUIRED_FIELDS = ['title', 'description', 'author', 'date', 'uid'];
const DATE_RE = /^\d{2}\/\d{2}\/\d{4}$/;

function walk(dir, out) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (/\.mdx?$/.test(entry.name)) out.push(full);
  }
  return out;
}

function parseFrontMatter(content) {
  if (!content.startsWith('---\n') && !content.startsWith('---\r\n')) return null;
  const end = content.indexOf('\n---', 4);
  if (end === -1) return null;
  const block = content.slice(4, end);
  const data = {};
  for (const line of block.split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (m) data[m[1]] = m[2].trim();
  }
  return data;
}

const files = walk(DOCS_ROOT, []);
const seenUid = new Map();
const seenSlug = new Map();
const results = [];

for (const file of files) {
  const base = path.basename(file);
  const rel = path.relative(DOCS_ROOT, file);
  // Partial/include files (prefixed with _) are not standalone pages and are exempt.
  if (base.startsWith('_')) continue;

  const content = fs.readFileSync(file, 'utf8');
  const fm = parseFrontMatter(content);
  const issues = [];

  if (!fm) {
    issues.push('missing front matter block');
  } else {
    for (const field of REQUIRED_FIELDS) {
      if (!fm[field]) issues.push(`missing required front matter field: ${field}`);
    }
    if (fm.date && !DATE_RE.test(fm.date)) {
      issues.push(`date "${fm.date}" does not match MM/DD/YYYY format`);
    }
    if (fm.description && fm.description.length < 40) {
      issues.push('description is shorter than 40 characters (weak for SEO)');
    }
    if (fm.description && fm.description.length > 160) {
      issues.push('description is longer than 160 characters (may be truncated in search results)');
    }
    if (fm.uid) {
      if (seenUid.has(fm.uid)) issues.push(`duplicate uid "${fm.uid}" (also used by ${seenUid.get(fm.uid)})`);
      else seenUid.set(fm.uid, rel);
    }
    if (fm.slug) {
      if (seenSlug.has(fm.slug)) issues.push(`duplicate slug "${fm.slug}" (also used by ${seenSlug.get(fm.slug)})`);
      else seenSlug.set(fm.slug, rel);
    }
  }

  results.push({ file: rel, issues });
}

process.stdout.write(JSON.stringify(results, null, 2));
