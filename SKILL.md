---
name: ui-handoff
description: Turn UI screenshots, static mockups, Figma exports, or design references into implementation-ready UI handoff specs for AI coding agents. Use when the user provides a design image and needs components, layout regions, design tokens, interaction states, responsive rules, AI freedom constraints, and acceptance criteria before building frontend code.
---

# UI Handoff

Convert static UI references into a structured spec that another AI agent can implement without guessing.

## Core Rule

Do not jump from screenshot to code. First produce a handoff package:

1. Visual inventory
2. Component model
3. Design tokens
4. Interaction and state model
5. Responsive behavior
6. AI freedom rules
7. Acceptance criteria

Use the schema in [references/schema.md](references/schema.md). For a complete example, load [references/example-handoff.md](references/example-handoff.md).

## Workflow

### 1. Classify the Surface

Identify the product type before extracting UI:

- product_app: dashboards, workspaces, admin tools, editors, SaaS apps
- commerce: product listings, checkout, catalog, booking
- content: blogs, docs, editorial, portfolio
- brand: landing pages, campaigns, marketing pages
- game_or_tool: interactive tools, games, simulations

This controls density, motion, layout, and freedom. Product apps should be quiet, scannable, and efficient; brand pages may be more expressive.

### 2. Extract Layout Regions

Name each visible region by role, not position alone:

- app_shell
- sidebar
- top_bar
- main_workspace
- right_panel
- bottom_bar
- modal
- drawer
- canvas
- data_table
- card_grid

For each region, record purpose, approximate dimensions, content density, scroll behavior, and collapse behavior.

### 3. Build Component Inventory

For every repeated or interactive element, define:

- component name
- role/purpose
- variants
- states
- props/data inputs
- exact/adaptive/creative freedom level
- implementation notes

Prefer reusable components over one-off div recreation.

### 4. Extract Design Tokens

Capture tokens in semantic roles:

- colors: background, surface, text, border, accent, status colors
- typography: page title, section title, body, caption, numeric/stat text
- spacing: base scale and common gaps
- radius: button, card, modal, input
- elevation: borders, shadows, overlays
- iconography: icon style, size, stroke, label rules
- motion: durations, easing, hover/selection feedback

If exact values are unavailable, estimate conservatively and mark confidence as estimated.

### 5. Define Interaction States

Static screenshots rarely show all states. Add the missing states explicitly:

- hover
- active/pressed
- selected
- focus-visible
- disabled
- loading
- empty
- error
- success
- unsaved changes

Do not invent major product behavior. Mark unclear behavior as an assumption.

### 6. Set AI Freedom Rules

Classify every area:

- exact: must match structure, scale, density, and style
- adaptive: may change for content/responsive needs while preserving design language
- creative: may be redesigned within the extracted design language
- placeholder: sample content only

Also list anti-patterns the implementation must avoid.

### 7. Produce Deliverables

Generate these sections:

1. ui-handoff.md: human-readable handoff
2. ui-handoff.json: machine-checkable schema
3. implementation-prompt.md: prompt for a coding agent
4. acceptance-checklist.md: verification gate

If the user only wants a quick answer, provide ui-handoff.md inline and skip files unless coding will follow.

## Output Contract

When creating files, use the template at [assets/templates/ui-handoff-template.md](assets/templates/ui-handoff-template.md).

Minimum JSON fields:

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

Validate JSON with:

    python3 scripts/validate_handoff.py path/to/ui-handoff.json

## Quality Gate

Before handing off to implementation, verify:

- Components are named by role, not only visual appearance.
- All interactive components include states.
- Design tokens use semantic roles.
- Exact/adaptive/creative areas are explicit.
- Mobile behavior is specified.
- Acceptance criteria include screenshot checks and overflow/overlap checks.
- Assumptions are separated from facts visible in the image.

