# Design Image Analysis Protocol

Use this protocol before writing the final UI handoff. The goal is to make screenshot interpretation explicit, evidence-based, and repeatable.

## Analysis Passes

### 1. Whole-Image Pass

Capture the global structure before details:

- product/surface type
- primary user task
- viewport orientation and approximate density
- major regions and their visual priority
- obvious navigation model
- visible repeated patterns
- visible constraints, such as fixed shell, scroll areas, side panels, or canvas

Output:

    {
      "pass": "whole_image",
      "findings": [],
      "confidence": "high | medium | low",
      "assumptions": []
    }

### 2. Region Segmentation Pass

Split the design into semantic regions. Do not describe only positions.

Good region names:

- app_shell
- sidebar
- top_bar
- command_bar
- main_workspace
- content_panel
- inspector_panel
- right_panel
- bottom_bar
- modal
- drawer
- canvas
- timeline
- data_table
- card_grid

For each region, capture:

- purpose
- boundary evidence
- approximate size/proportion
- scroll behavior
- relationship to other regions
- responsive expectation

### 3. Text and Hierarchy Pass

Extract visible text and infer hierarchy:

- page title
- section titles
- nav labels
- tabs/segmented controls
- button labels
- field labels
- table headers
- metadata
- empty/error/helper text

If OCR tooling is available, use it. If not, manually transcribe visible text from the image. Mark uncertain text as uncertain.

Use text hierarchy to infer typography tokens, not decoration.

### 4. Component Boundary Pass

Identify reusable components from repeated structure, not just visual similarity.

For each candidate component:

- name by role
- repeated instances
- internal slots
- variants
- data inputs/props
- visible states
- missing but required states
- exact/adaptive/creative freedom

Examples:

- SidebarNavItem
- WorkspaceCard
- InspectorSection
- FilterButton
- SearchInput
- DataTableRow
- MetricTile
- TimelineEvent

### 5. Design Token Pass

Extract or estimate semantic tokens:

- color roles
- type scale
- spacing scale
- radius
- elevation/border rules
- icon style
- density rules
- motion rules

Do not claim exact pixel values unless measured. Use confidence values:

- observed: directly visible or measured
- estimated: inferred from screenshot
- assumed: needed for implementation but not visible

### 6. Interaction Inference Pass

Infer behavior only from visual evidence and product conventions. Separate facts from assumptions.

For each interactive candidate:

- why it appears interactive
- likely action
- required states
- missing states to implement
- keyboard/accessibility expectation
- risk if guessed wrong

Required state checklist:

- hover
- active/pressed
- selected
- focus-visible
- disabled
- loading
- empty
- error
- success
- unsaved changes, if editing is implied

### 7. Freedom Map Pass

Mark every major area:

- exact: preserve structure, scale, density, and style
- adaptive: preserve design language; adjust for responsive/content needs
- creative: AI may redesign within the extracted language
- placeholder: sample content only

Also list forbidden inventions, such as marketing heroes, decorative blobs, nested cards, unrelated gradients, or new navigation.

### 8. Asset Decomposition Pass

If the design contains reusable raster assets, sprites, maps, icon sheets, HUD art, or FX, add asset_decomposition. See [asset-tools.md](asset-tools.md).

Skip this pass for ordinary product UI unless assets need extraction.

### 9. Implementation Prompt Pass

Convert the analysis into a coding prompt:

- target surface and user task
- component architecture
- token rules
- interaction states
- responsive rules
- freedom map
- screenshot QA requirements

The prompt should tell a coding agent what to build, what not to invent, and how to verify.

### 10. QA Pass

Define verification before implementation:

- desktop screenshot viewport
- mobile screenshot viewport
- no text overflow
- no component overlap
- stable dimensions for fixed controls
- all required states present
- design tokens reused
- exact areas preserved
- assumptions reviewed

## Evidence Rules

Use these labels:

- visible: directly visible in the image
- inferred: strongly implied by repeated pattern or product convention
- assumed: necessary implementation choice not visible in the image
- unknown: cannot be determined from the image

Never hide uncertainty. Put unknown or assumed items in the assumptions section.

## Minimum Analysis Output

Every serious design-image handoff should include:

    {
      "analysis_passes": [
        "whole_image",
        "region_segmentation",
        "text_hierarchy",
        "component_boundaries",
        "design_tokens",
        "interaction_inference",
        "freedom_map",
        "implementation_prompt",
        "qa"
      ],
      "evidence": [],
      "assumptions": [],
      "unknowns": []
    }

