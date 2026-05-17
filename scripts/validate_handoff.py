#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "page_intent",
    "layout_regions",
    "component_inventory",
    "design_tokens",
    "interaction_states",
    "responsive_rules",
    "ai_freedom_rules",
    "acceptance_criteria",
]

LIST_FIELDS = [
    "layout_regions",
    "component_inventory",
    "interaction_states",
    "responsive_rules",
    "ai_freedom_rules",
    "acceptance_criteria",
]

FREEDOMS = {"exact", "adaptive", "creative", "placeholder"}


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) != 2:
        return fail("usage: validate_handoff.py path/to/ui-handoff.json")

    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f"file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")

    if not isinstance(data, dict):
        return fail("top-level JSON must be an object")

    missing = [field for field in REQUIRED_TOP_LEVEL if field not in data]
    if missing:
        return fail("missing required fields: " + ", ".join(missing))

    for field in LIST_FIELDS:
        if not isinstance(data[field], list) or not data[field]:
            return fail(f"{field} must be a non-empty array")

    if not isinstance(data["page_intent"], dict) or not data["page_intent"]:
        return fail("page_intent must be a non-empty object")

    if not isinstance(data["design_tokens"], dict) or not data["design_tokens"]:
        return fail("design_tokens must be a non-empty object")

    for idx, region in enumerate(data["layout_regions"]):
        if not isinstance(region, dict):
            return fail(f"layout_regions[{idx}] must be an object")
        for key in ["id", "role"]:
            if key not in region:
                return fail(f"layout_regions[{idx}] missing {key}")
        if "freedom" in region and region["freedom"] not in FREEDOMS:
            return fail(
                f"layout_regions[{idx}] freedom '{region['freedom']}' must be one of {sorted(FREEDOMS)}"
            )

    component_names = []
    for idx, component in enumerate(data["component_inventory"]):
        if not isinstance(component, dict):
            return fail(f"component_inventory[{idx}] must be an object")
        for key in ["name", "role", "states", "freedom"]:
            if key not in component:
                return fail(f"component_inventory[{idx}] missing {key}")
        if component["freedom"] not in FREEDOMS:
            return fail(
                f"component_inventory[{idx}] freedom '{component['freedom']}' must be one of {sorted(FREEDOMS)}"
            )
        if not component["states"]:
            return fail(f"component_inventory[{idx}] must define at least one state")
        component_names.append(component["name"])

    component_name_set = set(component_names)
    for idx, state in enumerate(data["interaction_states"]):
        if not isinstance(state, dict):
            return fail(f"interaction_states[{idx}] must be an object")
        for key in ["component", "state"]:
            if key not in state:
                return fail(f"interaction_states[{idx}] missing {key}")
        if state["component"] not in component_name_set:
            return fail(
                f"interaction_states[{idx}] references component '{state['component']}' "
                f"which is not in component_inventory"
            )

    for idx, rule in enumerate(data["ai_freedom_rules"]):
        if not isinstance(rule, dict):
            return fail(f"ai_freedom_rules[{idx}] must be an object")
        if rule.get("freedom") not in FREEDOMS:
            return fail(f"ai_freedom_rules[{idx}] has invalid freedom level")

    print(
        f"PASS: {path} is a valid UI handoff "
        f"({len(component_names)} components, {len(data['interaction_states'])} states)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
