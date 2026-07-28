# <!-- TODO: Project Name -->

<!-- TODO: One-line project description -->

## Overview

<!-- TODO: Describe what this project does and why it exists -->

## Getting Started

### Prerequisites

<!-- TODO: List prerequisites (e.g., tools, accounts, access) -->

### Installation

<!-- TODO: Installation steps -->

### Usage

<!-- TODO: Basic usage examples -->

### After cloning a project from this template

```sh
mise install      # Install pinned tool versions
lefthook install  # Wire up pre-commit hooks
just workspace    # Open the repo as a herdr workspace (optional)
```

### Development workspace

`.herdr/layout.json` declares a [herdr](https://herdr.dev) workspace for this
repo — editor, agent, `just --list`, and a live `git status` pane. `just
workspace` opens it; re-running rebuilds it in place rather than duplicating it.

The file is herdr's own `LayoutNode` tree, so herdr's documentation is the
reference and a layout you arrange by hand can be exported with the socket API's
`layout.export` and pasted back. `${REPO}`, `${REPO_NAME}` and `${HOME}` expand
at apply time, so it works wherever the repo is cloned.

Edit it to fit the project — a service might want a `dev server` pane, a data
repo a DuckDB REPL. `just check-workspace` validates it, and the same check runs
as a pre-commit hook. Delete the file to fall back to the machine-wide default.

Entirely optional: it costs nothing if you don't use herdr, and nothing in the
build depends on it. `just workspace` needs `herdr-up`, which ships with the
[dotfiles](https://github.com/jameskazie/dotfiles).

CI is on observe mode by default. To switch to enforce, follow [the rollout SOP](https://github.com/Diixtra/diixtra-forge/blob/main/docs/code-quality/rollout.md) once the baseline is clean.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## Security

See [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

## License

<!-- TODO: Choose one of the following based on repo visibility -->
<!-- For public repos: -->
This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
<!-- For private repos, replace with: -->
<!-- All rights reserved. -->
