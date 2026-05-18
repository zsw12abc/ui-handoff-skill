---
name: ui-handoff
description: Turn UI screenshots, static mockups, Figma exports, or design references into implementation-ready UI handoff specs for AI coding agents. Use when the user provides a design image and needs components, layout regions, design tokens, interaction states, responsive rules, AI freedom constraints, and acceptance criteria before building frontend code.
version: 0.2.0
---

# UI Handoff

Convert a static UI reference into a structured spec another AI agent can implement without inventing.

For install, update, and release docs see [README.md](README.md).

## Core Rule

Never jump from screenshot to code. First produce a handoff package covering:

1. Page intent and surface classification
2. Layout regions
3. Component inventory
4. Design tokens
5. Interaction states
6. Responsive rules
7. Accessibility checks
8. AI freedom rules (exact / adaptive / creative / placeholder)
9. Acceptance criteria
10. Asset decomposition — only if raster/sprite/map assets are present

Separate **evidence** (visible in the image) from **assumptions** (needed for implementation but not visible). Never hide uncertainty.

## Mode Selection

- **Quick mode** — user wants a fast answer or a single small screen. Produce `ui-handoff.md` inline; skip the JSON file and validator. Still tag freedom rules and list assumptions.
- **Full mode** — user will hand off to a coding agent, or the surface is non-trivial. Produce all four deliverables (see Output below) and run the validator.

Default to Quick mode unless the user signals implementation will follow.

## Inputs

- Pasted/attached screenshot
- Figma export, design image URL, or mockup file
- Optional Figma MCP if connected — fetch frame metadata when available rather than re-inferring from pixels

## Workflow

1. **Classify the surface** — `product_app | commerce | content | brand | game_or_tool`. This controls density, motion, layout, and freedom. Product apps stay quiet, scannable, efficient; brand pages may be expressive.
2. **Run the analysis protocol** in [references/design-image-analysis.md](references/design-image-analysis.md). Record evidence, assumptions, and unknowns separately.
3. **Extract regions, components, tokens, states, responsive rules, a11y checks, freedom rules, and acceptance criteria** per the schema in [references/schema.md](references/schema.md). Use the accessibility checklist in [references/accessibility.md](references/accessibility.md) — color contrast, focus-visible, touch targets, keyboard nav, ARIA roles, motion safety.
4. **Decompose visual assets** only when raster sprites, maps, icon packs, prop packs, or HUD art are present — see [references/asset-tools.md](references/asset-tools.md). Do not force the sprite pipeline for ordinary SaaS/dashboard/mobile UI.
5. **Produce deliverables** (Full mode) and validate.

## Naming Rules

- Components named by **role**, not visual appearance (`WorkspaceCard`, not `WhiteBox`).
- Layout regions named by **role**, not position alone (`inspector_panel`, not `right_thing`).
- Design tokens in **semantic roles** (`text_secondary`, `surface`, `accent`), not raw colors.
- Every interactive component must list its states; missing states (hover, focus-visible, disabled, loading, empty, error) are added explicitly even if not in the image.

## Output Contract

Full mode generates:

1. `ui-handoff.md` — human-readable, using [assets/templates/ui-handoff-template.md](assets/templates/ui-handoff-template.md)
2. `ui-handoff.json` — machine-checkable, matches [references/schema.md](references/schema.md)
3. `implementation-prompt.md` — prompt for the coding agent
4. `acceptance-checklist.md` — verification gate

Required JSON fields (enforced by the validator):

    {
      "page_intent": {},
      "layout_regions": [],
      "component_inventory": [],
      "design_tokens": {},
      "interaction_states": [],
      "responsive_rules": [],
      "ai_freedom_rules": [],
      "acceptance_criteria": []
    }

Recommended additional fields: `analysis`, `accessibility`, `asset_decomposition` — see [references/schema.md](references/schema.md).

Validate:

    python scripts/validate_handoff.py path/to/ui-handoff.json

The validator checks required fields, freedom enums on regions/components/rules, and that every `interaction_states.component` references a name in `component_inventory`.

## Quality Gate

Before handing off to implementation, verify:

- Components named by role, not appearance.
- All interactive components include states.
- Design tokens use semantic roles.
- Exact / adaptive / creative areas are explicit.
- Mobile behavior is specified.
- Accessibility checks completed (contrast, focus order, touch targets).
- Acceptance criteria include screenshot and overflow/overlap checks.
- Assumptions are separated from facts visible in the image.

## Feedback Capture (self-improvement)

This skill keeps a feedback log so future invocations can be optimized against real gaps, not guesses. **Log on the spot** — silent failures don't get fixed.

**When to log** — call `scripts/log_feedback.py` whenever the user:

- Corrects the handoff ("you missed X", "this should be Y", "wrong freedom level for Z").
- Points out something the skill doesn't cover (a missing field, an unhandled surface type, a validator false-positive/negative).
- Has to manually rewrite a section of the generated spec.
- Explicitly says "remember this" / "记下来" / "feedback for the skill".

Also log a confirmation entry (severity `low`, tag `validated`) when the user explicitly approves a non-obvious choice — `"--message='quick mode was the right call for this single-screen ask'"`. Successes are signal too; only logging corrections drifts the skill toward over-caution.

**Do not log** routine in-conversation tweaks where the user is just iterating on the artifact (e.g. "rename this token") — those are about the current spec, not about the skill.

**Call format** — use the project's Python:

    python scripts/log_feedback.py \
      --message "validator didn't catch a component referenced by an interaction state with a typo" \
      --severity high \
      --tags "validator,naming" \
      --context "settings page handoff in product_app surface" \
      --skill-version 0.2.0

Severity: `high` = blocks the handoff or misleads the implementing agent; `med` = noticeable friction; `low` = polish or confirmation. Tags are free-form but reuse existing ones when possible (`validator`, `a11y`, `tokens`, `freedom-rules`, `responsive`, `naming`, `assets`, `mode-selection`, `validated`).

The script writes to `~/.claude/skill-feedback/ui-handoff/feedback.jsonl` (user-level, so feedback from any project surfaces here when you come back to optimize).

## Optimization Mode

Triggered when, inside the skill's own repo, the user asks to **optimize / improve / review feedback for / iterate on** the skill (in English or Chinese — e.g. "优化这个 skill", "review feedback").

Steps:

1. Read the log: `python scripts/show_feedback.py` (add `--since 30d` once the log is large).
2. Cluster entries by tag and severity. Surface every `high`-severity item and any tag with 3+ entries; ignore singleton `low` items unless they form a pattern.
3. For each cluster, propose a specific edit (which file, which section, what to add/remove). Do not invent improvements that aren't backed by a logged entry — the point is to ground optimization in real usage.
4. Confirm the plan with the user before editing. After applying, bump the `version:` field in this file's frontmatter (patch for fixes, minor for new sections or new validator rules).
5. Do **not** delete log entries after acting on them — they're history. If you want to mark items addressed, add a sibling file `~/.claude/skill-feedback/ui-handoff/addressed.jsonl` with the original `ts` and the commit SHA that addressed it.

## Related Skills

- `design:accessibility-review` — deeper WCAG 2.1 AA audit; pair with this skill before final handoff.
- `design:design-critique` — feedback on hierarchy and consistency before locking the spec.
- `design:design-handoff` — generic dev-facing handoff; use that when the consumer is a human, not an AI coding agent.
