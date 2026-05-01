# AGENTS.md

This repo follows the Diixtra org-wide coding guidelines. The `diixtra-coding-guidelines` skill in `~/.claude/skills/` defines the principles (root-cause-first, layered TDD, security-in-depth, complete solutions, continuous evolution) and per-language modules.

## Code-quality automation

This repo participates in the four-slot org code-quality framework:

1. **Pre-commit hooks** — `lefthook.yml` at the repo root. Run `lefthook install` after cloning. Trim language sections this repo doesn't use.
2. **CI** — `.github/workflows/code-quality.yaml` calls the org-wide reusable workflow at `Diixtra/diixtra-forge/.github/workflows/code-quality.yaml@main`. Defaults to `mode: observe` (advisory). Flip to `mode: enforce` per the SOP at https://github.com/Diixtra/diixtra-forge/blob/main/docs/code-quality/rollout.md once findings are clean.
3. **Renovate** — already configured org-wide.
4. **Skill** — `code-review-triage` in `~/.claude/skills/` interprets CI findings into the four-outcome decision (fix / track / suppress / reject).

## Guideline overrides

If this repo needs to override an org-module rule, document it here under a `## Guideline Overrides` section per the diixtra-coding-guidelines skill template. Temporary overrides must link to an issue.
