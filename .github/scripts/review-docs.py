#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = ROOT / ".github" / "SKILL.md"


def run(cmd, env=None):
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)


def collect_changed_files():
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if not base_ref:
        return []
    pr_head = os.environ.get("GITHUB_SHA", "HEAD")
    result = run(["git", "diff", "--name-only", f"origin/{base_ref}...{pr_head}"])
    if result.returncode != 0:
        return []
    return [p.strip() for p in result.stdout.splitlines() if p.strip() and (p.endswith(".md") or p.endswith(".mdx"))]


def read_skill():
    return SKILL_PATH.read_text(encoding="utf-8")


def build_prompt(files, skill):
    file_list = "\n".join(f"- {f}" for f in files)
    return f"""You are a documentation reviewer for a GitHub pull request.

Review the following Markdown or MDX files and provide concise, actionable review comments.
Focus on correctness, clarity, style, markdown syntax, and broken links or formatting issues.
Do not rewrite the whole document. Keep feedback targeted.

Repository instructions:
{skill}

Files to review:
{file_list}

Return JSON only with this schema:
{{"comments": [{{"path": "file/path.md", "line": 1, "body": "Your review comment"}}]}}
"""


def main():
    files = collect_changed_files()
    if not files:
        print("No markdown files changed; skipping review.")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not configured; skipping review.")
        return

    skill = read_skill()
    prompt = build_prompt(files, skill)

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a precise technical documentation reviewer."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    response = run(
        [
            "python3",
            "-c",
            "import json,sys,urllib.request;"
            "req=urllib.request.Request('https://api.openai.com/v1/chat/completions', data=json.dumps(json.loads(sys.argv[1])).encode(), headers={'Authorization':'Bearer ' + os.environ['OPENAI_API_KEY'], 'Content-Type':'application/json'});"
            "resp=urllib.request.urlopen(req, timeout=60);"
            "print(resp.read().decode())",
            json.dumps(payload),
        ],
        env=os.environ.copy(),
    )

    if response.returncode != 0:
        print(response.stderr)
        sys.exit(response.returncode)

    try:
        content = json.loads(response.stdout)
        choices = content["choices"]
        if not choices:
            raise ValueError("No choices returned")
        message = choices[0]["message"]["content"]
        review = json.loads(message)
        comments = review.get("comments", [])
    except Exception as exc:
        print(f"Failed to parse AI response: {exc}")
        sys.exit(0)

    if not comments:
        print("No review comments generated.")
        return

    out_path = ROOT / ".github" / "review-comments.json"
    out_path.write_text(json.dumps(comments, indent=2), encoding="utf-8")
    print(f"Wrote {len(comments)} review comments to {out_path}")


if __name__ == "__main__":
    main()
