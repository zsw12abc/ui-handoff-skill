# Example UI Handoff

This is a compact example for a product workspace screenshot.

## Page Intent

- Surface type: product_app
- User goal: Review and act on work items from a central workspace.
- Design register: product
- Density: compact
- Mood: calm, focused, operational
- Must not do: marketing hero, decorative backgrounds, nested cards, oversized typography

## Layout Regions

| ID | Role | Position | Priority | Scroll | Responsive | Freedom |
|---|---|---:|---:|---|---|---|
| app_shell | contains navigation and workspace | full page | 1 | body locked | keeps app frame | exact |
| sidebar | primary navigation | left | 2 | internal if needed | collapses to icon rail | exact |
| top_bar | view title and actions | top center | 2 | fixed | actions move to overflow | exact |
| main_workspace | task content | center | 1 | vertical | full width on mobile | adaptive |
| right_panel | details and context | right | 3 | internal | drawer below 900px | adaptive |

## Component Inventory

| Component | Role | Variants | States | Props/Data | Freedom | Notes |
|---|---|---|---|---|---|---|
| SidebarNavItem | switch workspace sections | default, selected, disabled | hover, selected, focus | icon, label, count | exact | stable height; no layout shift |
| WorkspaceCard | summarize item | default, selected, warning | hover, selected, loading | title, status, metadata | exact | same radius/padding across cards |
| FilterButton | open filters | default, active | hover, pressed, focus | label, icon, activeCount | exact | active state must be visible |
| DetailPanel | show selected item details | default, empty | loading, empty, error | selectedItem | adaptive | mobile drawer |

## Design Tokens

Colors should be emitted as semantic roles such as background, surface, border, text_primary, text_secondary, and accent. Values may be estimated when the source is a flat screenshot.

## Acceptance Criteria

- Desktop 1440x900 screenshot matches shell proportions.
- Mobile 390x844 screenshot has no overlap.
- Sidebar, cards, buttons, tabs, and panel states are implemented.
- All colors and spacing come from tokens.

