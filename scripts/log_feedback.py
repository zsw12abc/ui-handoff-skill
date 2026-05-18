#!/usr/bin/env python3
"""Append a single feedback entry about the ui-handoff skill.

Writes to ~/.claude/skill-feedback/ui-handoff/feedback.jsonl as one JSON
object per line. Safe to call concurrently from short-lived invocations.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

SKILL = "ui-handoff"
SEVERITIES = {"low", "med", "high"}
LOG_DIR = Path.home() / ".claude" / "skill-feedback" / SKILL
LOG_FILE = LOG_DIR / "feedback.jsonl"


def git_remote(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, timeout=2,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Log feedback about the ui-handoff skill.")
    ap.add_argument("--message", "-m", required=True, help="What was wrong / missing / awkward.")
    ap.add_argument("--severity", "-s", default="med", choices=sorted(SEVERITIES))
    ap.add_argument("--tags", "-t", default="", help="Comma-separated tags, e.g. 'validator,a11y'.")
    ap.add_argument("--context", "-c", default="", help="Optional one-line context (surface, what was being produced).")
    ap.add_argument("--skill-version", default="", help="Version of the skill at time of feedback (from SKILL.md frontmatter).")
    args = ap.parse_args()

    cwd = Path(os.getcwd())
    entry = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "skill": SKILL,
        "skill_version": args.skill_version,
        "severity": args.severity,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "message": args.message.strip(),
        "context": args.context.strip(),
        "cwd": str(cwd),
        "git_remote": git_remote(cwd),
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"logged feedback to {LOG_FILE}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
