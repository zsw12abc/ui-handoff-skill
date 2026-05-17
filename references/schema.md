# UI Handoff Schema

Use this schema as the canonical output shape. JSON is preferred for machine handoff; Markdown may mirror the same sections for humans.

## Top-Level Fields

### page_intent

Required object. Example:

    {
      "surface_type": "product_app",
      "user_goal": "Manage work items in a dense workspace",
      "design_register": "product",
      "density": "compact | standard | spacious",
      "mood": "calm, utilitarian, focused",
      "must_not_do": ["marketing hero", "decorative gradient blobs"]
    }

### analysis

Recommended object for serious screenshot handoff. It records how the design image was interpreted.

    {
      "analysis_passes": [
        "whole_image",
        "region_segmentation",
        "text_hierarchy",
        "component_boundaries",
        "design_tokens",
        "interaction_inference",
        "freedom_map",
        "qa"
      ],
      "evidence": [
        {
          "claim": "The left rail is primary navigation",
          "basis": "visible repeated nav rows with selected state",
          "confidence": "high",
          "type": "visible"
        }
      ],
      "assumptions": [],
      "unknowns": []
    }

### layout_regions

Required array. Each item:

    {
      "id": "main_workspace",
      "role": "primary content and task surface",
      "position": "center",
      "visual_priority": 1,
      "approx_size": "fills remaining width",
      "scroll_behavior": "vertical content scroll",
      "responsive_behavior": "becomes full width below 900px",
      "freedom": "adaptive"
    }

### component_inventory

Required array. Each item:

    {
      "name": "WorkspaceCard",
      "role": "summarize a work item",
      "instances_visible": 6,
      "variants": ["default", "selected", "warning"],
      "states": ["hover", "selected", "loading", "empty"],
      "props": ["title", "status", "metadata", "actions"],
      "freedom": "exact",
      "notes": "Use same padding/radius for all cards."
    }

### design_tokens

Required object with colors, typography, spacing, radius, and elevation when visible or inferable.

### interaction_states

Required array. Each item:

    {
      "component": "SidebarNavItem",
      "state": "selected",
      "visual_change": "active background, stronger text/icon color",
      "behavior": "switch workspace view",
      "required": true
    }

### responsive_rules

Required array.

    {
      "breakpoint": "below 900px",
      "rule": "right panel becomes drawer; sidebar collapses to icons",
      "priority": "required"
    }

### ai_freedom_rules

Required array.

    {
      "area": "main workspace card contents",
      "freedom": "adaptive",
      "allowed": ["adjust sample data", "wrap metadata"],
      "forbidden": ["change card radius", "add decorative gradients"]
    }

### acceptance_criteria

Required array.

    {
      "id": "desktop-screenshot",
      "criterion": "Desktop screenshot visually matches layout, density, and hierarchy",
      "verification": "Playwright screenshot at 1440x900",
      "required": true
    }

### asset_decomposition

Optional array. Include only when the design reference contains reusable raster assets, game sprites, maps, prop packs, icon sheets, FX, or HUD art that should be extracted or regenerated outside the normal UI component pipeline.

    {
      "id": "player_sprite_sheet",
      "source_region": "lower-left animation strip",
      "asset_type": "sprite_sheet",
      "strategy": "sprite-sheet split and transparent cleanup",
      "recommended_tool": "agent-sprite-forge/generate2dsprite",
      "outputs": ["transparent PNG frames", "GIF preview", "metadata JSON"],
      "notes": "Preserve frame count and animation cadence."
    }

## Freedom Levels

- exact: preserve visual structure, relative spacing, density, and component style.
- adaptive: preserve intent and design language; adjust for content or responsive behavior.
- creative: free to design within the system.
- placeholder: temporary content; do not treat as product logic.

## Confidence

Use observed when directly visible in the image. Use estimated when inferred from pixels. Use assumed when needed for implementation but not visible.
