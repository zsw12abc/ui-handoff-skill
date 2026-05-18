#!/usr/bin/env python3
"""Read and group feedback collected by log_feedback.py.

Default output is grouped by tag with high-severity items first, so the
optimization pass can see recurring themes at a glance. Pass --format json
to get the raw list for programmatic consumption.
"""
import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LOG_FILE = Path.home() / ".claude" / "skill-feedback" / "ui-handoff" / "feedback.jsonl"
SEVERITY_ORDER = {"high": 0, "med": 1, "low": 2}


def parse_since(s: str) -> dt.datetime | None:
    if not s:
        return None
    m = re.fullmatch(r"(\d+)([dhw])", s.strip().lower())
    if not m:
        raise ValueError(f"--since must look like '7d', '24h', or '2w' (got {s!r})")
    n, unit = int(m.group(1)), m.group(2)
    delta = {"d": dt.timedelta(days=n), "h": dt.timedelta(hours=n), "w": dt.timedelta(weeks=n)}[unit]
    return dt.datetime.now(dt.timezone.utc) - delta


def load_entries(since: dt.datetime | None) -> list[dict]:
    if not LOG_FILE.exists():
        return []
    out = []
    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since:
            try:
                ts = dt.datetime.fromisoformat(entry.get("ts", ""))
            except ValueError:
                continue
            if ts < since:
                continue
        out.append(entry)
    return out


def print_grouped(entries: list[dict]) -> None:
    if not entries:
        print("(no feedback recorded yet)")
        return

    by_tag: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        for tag in e.get("tags") or ["untagged"]:
            by_tag[tag].append(e)

    tag_counts = Counter({t: len(v) for t, v in by_tag.items()})
    sev_counts = Counter(e.get("severity", "med") for e in entries)

    print(f"{len(entries)} entries · severity: " +
          ", ".join(f"{k}={sev_counts.get(k, 0)}" for k in ("high", "med", "low")))
    print()

    for tag, _ in tag_counts.most_common():
        items = sorted(by_tag[tag], key=lambda e: (SEVERITY_ORDER.get(e.get("severity", "med"), 3), e.get("ts", "")))
        print(f"## {tag}  ({len(items)})")
        for e in items:
            sev = e.get("severity", "med")
            ts = e.get("ts", "")[:10]
            ctx = f" — {e['context']}" if e.get("context") else ""
            print(f"  [{sev}] {ts}: {e.get('message', '').strip()}{ctx}")
        print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Show ui-handoff feedback log.")
    ap.add_argument("--since", default="", help="Only entries newer than this, e.g. '7d', '24h', '2w'.")
    ap.add_argument("--tag", default="", help="Only entries matching this tag.")
    ap.add_argument("--format", choices=["grouped", "json"], default="grouped")
    args = ap.parse_args()

    try:
        since = parse_since(args.since)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    entries = load_entries(since)
    if args.tag:
        entries = [e for e in entries if args.tag in (e.get("tags") or [])]

    if args.format == "json":
        json.dump(entries, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_grouped(entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
