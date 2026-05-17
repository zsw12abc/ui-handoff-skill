---
name: ui-handoff
description: Turn UI screenshots, static mockups, Figma exports, or design references into implementation-ready UI handoff specs for AI coding agents. Use when the user provides a design image and needs components, layout regions, design tokens, interaction states, responsive rules, AI freedom constraints, and acceptance criteria before building frontend code.
version: 0.1.0
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

Minimum JSON shape:

    {
      "page_intent": {},
      "layout_regions": [],
      "component_inventory": [],
      "design_tokens": {},
      "interaction_states": [],
      "responsive_rules": [],
      "accessibility": {},
      "ai_freedom_rules": [],
      "acceptance_criteria": []
    }

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

## Related Skills

- `design:accessibility-review` — deeper WCAG 2.1 AA audit; pair with this skill before final handoff.
- `design:design-critique` — feedback on hierarchy and consistency before locking the spec.
- `design:design-handoff` — generic dev-facing handoff; use that when the consumer is a human, not an AI coding agent.
