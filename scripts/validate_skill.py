#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    path = Path("SKILL.md")
    if not path.exists():
        return fail("SKILL.md not found")

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return fail("SKILL.md must start with YAML frontmatter")

    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError:
        return fail("SKILL.md frontmatter is not closed")

    fields = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()

    for field in ["name", "description", "version"]:
        if not fields.get(field):
            return fail(f"missing frontmatter field: {field}")

    if fields["name"] != "ui-handoff":
        return fail("name must be ui-handoff")

    if not re.fullmatch(r"\d+\.\d+\.\d+", fields["version"]):
        return fail("version must use semver format, e.g. 0.1.0")

    required_phrases = [
        "npx skills add zsw12abc/ui-handoff-skill -y",
        "npx skills update ui-handoff",
        "npx skills add zsw12abc/ui-handoff-skill@v0.1.0 -y",
    ]
    for phrase in required_phrases:
        if phrase not in body:
            return fail(f"missing install/update instruction: {phrase}")

    print(f"PASS: SKILL.md metadata valid (version {fields['version']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

