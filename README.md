# ui-handoff-skill

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that turns UI screenshots, static mockups, or Figma exports into structured handoff specs an AI coding agent can implement without guessing.

The output covers components, layout regions, design tokens, interaction states, responsive rules, accessibility checks, and explicit **AI freedom rules** (exact / adaptive / creative / placeholder) so the implementing agent knows what it must preserve versus what it may redesign.

## How this differs from generic design handoff

Most "design handoff" docs target human developers. `ui-handoff` is shaped for the AI coding agent that will write the code:

- **Freedom rules** — every region/component is tagged `exact | adaptive | creative | placeholder` to fence what the agent may invent.
- **Evidence vs assumptions** — every claim from the screenshot is labeled `visible | inferred | assumed | unknown` so the agent doesn't treat guesses as facts.
- **JSON schema + validator** — `scripts/validate_handoff.py` checks the spec before it's handed off, catching missing states, undefined component references, and bad freedom levels.
- **Asset decomposition** — for game/raster assets, routes work to [Agent Sprite Forge](https://github.com/0x0funky/agent-sprite-forge) rather than treating sprites like product UI.

## Install

Latest stable:

    npx skills add zsw12abc/ui-handoff-skill -y

Pin a specific release:

    npx skills add zsw12abc/ui-handoff-skill@v0.2.0 -y

Update one skill:

    npx skills update ui-handoff

Update all installed skills:

    npx skills update

The installed version is in [SKILL.md](SKILL.md)'s `version:` frontmatter.

## Use

In Claude Code, paste or attach a design image and ask:

> Produce a UI handoff for this screen.

The skill triggers automatically when a design image is present and the request involves components, tokens, states, or implementation prep.

Run the validator on a generated spec:

    python scripts/validate_handoff.py path/to/ui-handoff.json

## Self-improvement loop

The skill records user feedback while it runs so it can be optimized later against real gaps. Logs land at `~/.claude/skill-feedback/ui-handoff/feedback.jsonl` (one JSON object per line) and are written by:

    python scripts/log_feedback.py -m "what was wrong" -s med -t "validator,a11y" -c "context"

To review what's accumulated:

    python scripts/show_feedback.py           # grouped by tag, high-severity first
    python scripts/show_feedback.py --since 30d --tag validator
    python scripts/show_feedback.py --format json

In this repo, ask the skill to **"review feedback"** or **"optimize this skill"** — it reads the log, clusters by tag/severity, and proposes specific edits backed by logged entries.

## Repository layout

| Path | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | The skill itself (auto-loaded into the model's context) |
| [references/schema.md](references/schema.md) | Canonical JSON shape and field definitions |
| [references/design-image-analysis.md](references/design-image-analysis.md) | 10-pass image analysis protocol |
| [references/accessibility.md](references/accessibility.md) | A11y checklist included in handoff |
| [references/asset-tools.md](references/asset-tools.md) | Raster/sprite/map decomposition routing |
| [references/example-handoff.md](references/example-handoff.md) | Compact worked example |
| [assets/templates/ui-handoff-template.md](assets/templates/ui-handoff-template.md) | Fill-in template for human-readable handoff |
| [examples/workspace-handoff.json](examples/workspace-handoff.json) | Reference JSON output |
| [scripts/validate_handoff.py](scripts/validate_handoff.py) | JSON validator |
| [scripts/validate_skill.py](scripts/validate_skill.py) | Skill metadata validator |

## Release

Cut a release by tagging the matching `version:` in [SKILL.md](SKILL.md):

    git tag v0.1.1
    git push origin v0.1.1

Or merge a commit with `[release]` in its message to `main` — the workflow reads the version from `SKILL.md` frontmatter, validates, and publishes zip + tar.gz artifacts.

## License

[MIT](LICENSE)
