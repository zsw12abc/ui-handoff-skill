# Accessibility Checklist

Include accessibility fields in every UI handoff. The goal is to surface the minimum that an AI coding agent must implement, not to substitute for a full WCAG audit. For a deep audit, escalate to the `design:accessibility-review` skill before final handoff.

## What to record in the handoff

Add an `accessibility` object to the JSON spec:

    {
      "accessibility": {
        "target_level": "WCAG 2.1 AA",
        "color_contrast": [
          {"pair": "text_primary on background", "ratio": "12.6:1", "passes": "AA"},
          {"pair": "text_secondary on surface", "ratio": "4.7:1", "passes": "AA"},
          {"pair": "accent on background", "ratio": "5.1:1", "passes": "AA-large"}
        ],
        "focus_order": [
          "sidebar nav",
          "top_bar search",
          "main_workspace cards",
          "right_panel actions"
        ],
        "focus_visible_required": true,
        "touch_targets": {
          "minimum": "44x44px",
          "exceptions": ["dense data-table rows allowed at 32px when keyboard-equivalent action exists"]
        },
        "keyboard_paths": [
          {"action": "select card", "keys": "Tab to focus, Enter to open"},
          {"action": "dismiss drawer", "keys": "Esc"}
        ],
        "aria_roles": [
          {"component": "SidebarNavItem", "role": "link", "notes": "aria-current=page on selected"},
          {"component": "WorkspaceCard", "role": "button", "notes": "aria-label from title"}
        ],
        "motion": {
          "respects_prefers_reduced_motion": true,
          "max_animation_duration_ms": 250
        },
        "assumptions": [
          "Exact color values are estimated from the screenshot; verify ratios against the implemented tokens."
        ]
      }
    }

## Checks to perform during the handoff pass

### Color contrast

- Body text on its background: ≥ 4.5:1 (AA).
- Large text (≥ 18.66px regular or 14px bold): ≥ 3:1 (AA-large).
- Non-text UI (focus rings, icon-only controls, form borders): ≥ 3:1 against adjacent color.
- Disabled controls are exempt but should still be visibly distinct from active.

When tokens are estimated from a screenshot, mark the ratio as `estimated` and add an assumption that values must be re-checked against the implemented palette.

### Focus

- Every interactive element has a visible focus indicator. Default to a 2px outline using `accent` at ≥ 3:1 against both the component background and the page background.
- Focus order follows visual reading order. List the expected tab path in `focus_order`.
- Modals and drawers trap focus; closing returns focus to the trigger.

### Keyboard

- Every mouse interaction has a keyboard equivalent. Record the keys in `keyboard_paths` for non-obvious flows (drag-and-drop, custom selection, hover-only menus).
- Esc dismisses overlays. Enter/Space activates buttons. Arrow keys move within composite widgets (tabs, menus, listboxes).

### Touch targets

- Minimum 44×44 CSS px for primary touch targets on mobile (per WCAG 2.5.5 AAA, treated as default here).
- Dense surfaces (data tables, compact toolbars) may go smaller if a keyboard or larger-target equivalent exists — record the exception.

### ARIA and semantics

- Prefer native HTML (`<button>`, `<a>`, `<input>`) over div-with-role.
- Icon-only controls require `aria-label`.
- Selected/expanded/checked state uses `aria-current`, `aria-expanded`, `aria-checked` — not just visual styling.

### Motion

- Animations honor `prefers-reduced-motion: reduce`.
- Default durations ≤ 250ms for UI feedback; longer transitions require justification.
- No infinite auto-playing motion in the main scanning path.

### Forms (if present)

- Every input has a programmatic label.
- Error messages are linked via `aria-describedby` and announced.
- Required fields are marked both visually and via `aria-required`.

## When to skip

If the design is a quick scratch or brand landing with no interactive elements, record `accessibility: { target_level: "WCAG 2.1 AA", notes: "static surface, only color contrast applies" }` and list contrast pairs. Do not skip the field entirely.
