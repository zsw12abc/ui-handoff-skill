# Asset Decomposition Tools

Use this reference when a UI screenshot contains reusable raster assets that should be separated, regenerated, sliced, or handed to a game/prototype pipeline.

## Agent Sprite Forge

Repository: https://github.com/0x0funky/agent-sprite-forge

Agent Sprite Forge provides Codex skills and scripts for game-ready 2D sprites, layered maps, and engine-ready prototypes.

Relevant included skills:

- generate2dsprite: sprites, animation sheets, props, spell bundles, FX, reference variants, fixed-frame sheets.
- generate2dmap: baked maps, layered raster maps, RPG maps, prop packs, collision/zones, Godot-editable scenes.

Typical outputs:

- raw sheet
- cleaned transparent sheet
- extracted frames
- PNG/GIF previews
- prop-pack slices
- placement/collision metadata
- engine handoff files

## When To Use It

Use Agent Sprite Forge when the design image includes:

- character sprites or animation sheets
- game HUD art with reusable icon/sprite assets
- tile maps, RPG maps, arena maps, or level mockups
- prop sheets or visual packs
- spell/projectile/impact FX
- transparent PNG asset extraction needs
- engine-ready Godot/Unity prototype handoff

Do not use it for ordinary product UI elements such as SaaS cards, nav items, forms, tables, dashboards, or standard icons unless the user explicitly wants raster asset extraction.

## Handoff Fields

Add an asset_decomposition section when needed:

    {
      "asset_decomposition": [
        {
          "id": "hud_icon_pack",
          "source_region": "top-right toolbar icons",
          "asset_type": "icon_pack",
          "strategy": "manual crop or regenerate as vector/icons",
          "recommended_tool": "native UI implementation",
          "outputs": ["lucide icons or inline SVG"],
          "notes": "Do not use sprite pipeline for standard app icons."
        },
        {
          "id": "player_sprite_sheet",
          "source_region": "character animation sheet",
          "asset_type": "sprite_sheet",
          "strategy": "sprite-sheet split and transparent cleanup",
          "recommended_tool": "agent-sprite-forge/generate2dsprite",
          "outputs": ["transparent PNG frames", "GIF preview", "metadata JSON"],
          "notes": "Preserve frame count, facing direction, and animation cadence."
        }
      ]
    }

## Decision Rules

- If the asset should become CSS/HTML/component code, keep it in the UI handoff.
- If the asset should become a transparent raster, animation frame sequence, map layer, or engine object, route it to Agent Sprite Forge.
- If the source screenshot is too low-resolution for extraction, specify regenerate-with-reference instead of pretending exact pixels are recoverable.
- Always preserve the visual identity and style lineage when using reference images.

