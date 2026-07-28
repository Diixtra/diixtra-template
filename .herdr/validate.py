#!/usr/bin/env python3
"""Validate a herdr layout file against herdr's LayoutNode shape.

Catches the failures that are otherwise silent or late: a layout that only fails
when applied (after the workspace already exists), a pane whose `command` is a
string rather than an argv array, a ratio outside 0..1, or a pane missing `cwd`
— which is the expensive one, because herdr fixes cwd at creation and has no
workspace.set_cwd, so such a pane silently inherits $HOME and stays there.

Stdlib only and no herdr binary required, so it runs in pre-commit and in CI on
runners that have never heard of herdr.

Usage: python3 .herdr/validate.py [.herdr/layout.json ...]
"""
from __future__ import annotations

import json
import sys

PLACEHOLDERS = ("${REPO}", "${REPO_NAME}", "${HOME}")


def check(node, path: str, errors: list[str]) -> None:
    if not isinstance(node, dict):
        errors.append(f"{path}: expected an object, got {type(node).__name__}")
        return

    kind = node.get("type")
    if kind == "pane":
        cwd = node.get("cwd")
        if cwd is None:
            errors.append(
                f"{path}: pane has no 'cwd' — it will inherit $HOME permanently "
                f"(herdr fixes cwd at creation). Use \"cwd\": \"${{REPO}}\"."
            )
        elif isinstance(cwd, str) and cwd.startswith("/") and not cwd.startswith(PLACEHOLDERS):
            errors.append(
                f"{path}: cwd {cwd!r} is an absolute path — use ${{REPO}} so the "
                f"layout works wherever the repo is cloned."
            )
        command = node.get("command")
        if command is not None and (
            not isinstance(command, list) or not all(isinstance(c, str) for c in command)
        ):
            errors.append(
                f"{path}: 'command' must be an array of strings "
                f'(e.g. ["bash", "-lc", "just test"]), got {type(command).__name__}'
            )
        env = node.get("env")
        if env is not None and (
            not isinstance(env, dict)
            or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items())
        ):
            errors.append(f"{path}: 'env' must be a string->string object")

    elif kind == "split":
        for key in ("direction", "ratio", "first", "second"):
            if key not in node:
                errors.append(f"{path}: split node is missing {key!r}")
        if node.get("direction") not in ("right", "down"):
            errors.append(
                f"{path}: direction must be 'right' or 'down', got {node.get('direction')!r}"
            )
        ratio = node.get("ratio")
        if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or not 0 < ratio < 1:
            errors.append(f"{path}: ratio must be a number strictly between 0 and 1, got {ratio!r}")
        if "first" in node:
            check(node["first"], f"{path}.first", errors)
        if "second" in node:
            check(node["second"], f"{path}.second", errors)

    else:
        errors.append(f"{path}: 'type' must be 'pane' or 'split', got {kind!r}")


def validate_file(path: str) -> int:
    try:
        with open(path) as fh:
            layout = json.load(fh)
    except FileNotFoundError:
        print(f"{path}: not found", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"{path}: invalid JSON — {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    check(layout, "root", errors)
    if errors:
        print(f"{path}: invalid herdr layout", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    panes: list[str] = []

    def collect(node):
        if node.get("type") == "pane":
            panes.append(node.get("label") or "(unlabelled)")
        else:
            collect(node["first"])
            collect(node["second"])

    collect(layout)
    print(f"{path}: ok — {len(panes)} panes ({', '.join(panes)})")
    return 0


def main(argv: list[str]) -> int:
    targets = argv[1:] or [".herdr/layout.json"]
    return max(validate_file(t) for t in targets)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
