#!/usr/bin/env python3
"""Format and lint-check a file after an agent or Tab edit (fail open)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from hook_log import log_hook

SCRIPT = "format-after-edit"

EXTENSIONS = {".css", ".html", ".js", ".json", ".jsx", ".md", ".svelte", ".ts", ".tsx"}
SKIP_DIR_NAMES = {".git", ".svelte-kit", "build", "dist", "node_modules"}
SKIP_FILE_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}


def resolve_path(raw: str, root: Path) -> Path | None:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve()
    except OSError:
        return None


def should_format(path: Path, root: Path) -> bool:
    if not path.is_file() or path.suffix not in EXTENSIONS:
        return False
    if path.name in SKIP_FILE_NAMES:
        return False
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return SKIP_DIR_NAMES.isdisjoint(path.parts)


def find_app_root(path: Path, repo: Path) -> Path | None:
    current = path.parent
    while True:
        prettier = current / "node_modules" / ".bin" / "prettier"
        if (current / "package.json").is_file() and prettier.is_file():
            return current
        if current == repo or current.parent == current:
            return None
        current = current.parent


def main() -> int:
    root = Path.cwd()
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        log_hook(SCRIPT, "afterFileEdit", result="skip", reason="invalid_json")
        sys.stdout.write("{}\n")
        return 0

    event = payload.get("hook_event_name") if isinstance(payload, dict) else None
    event_name = event if isinstance(event, str) and event else "afterFileEdit"
    file_path = payload.get("file_path") if isinstance(payload, dict) else None
    if not isinstance(file_path, str) or not file_path:
        log_hook(SCRIPT, event_name, result="skip", reason="no_file_path")
        sys.stdout.write("{}\n")
        return 0

    path = resolve_path(file_path, root)
    if path is None or not should_format(path, root):
        log_hook(SCRIPT, event_name, result="skip", reason="not_a_format_target", file=file_path)
        sys.stdout.write("{}\n")
        return 0

    app = find_app_root(path, root)
    if app is None:
        log_hook(SCRIPT, event_name, result="skip", reason="no_prettier", file=str(path))
        sys.stdout.write("{}\n")
        return 0

    prettier = app / "node_modules" / ".bin" / "prettier"
    common = {
        "cwd": app,
        "capture_output": True,
        "text": True,
        "timeout": 15,
        "check": False,
    }
    written = subprocess.run([str(prettier), "--write", "--log-level", "warn", str(path)], **common)
    checked = subprocess.run([str(prettier), "--check", "--log-level", "warn", str(path)], **common)
    log_hook(
        SCRIPT,
        event_name,
        result="formatted",
        file=str(path),
        write_exit=written.returncode,
        check_exit=checked.returncode,
    )

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
