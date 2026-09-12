#!/usr/bin/env python3
"""Run the colocated Vitest spec after an edit. Fail open. Do not start a server."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from hook_log import log_hook

SCRIPT = "run-related-tests"

SPEC_SUFFIXES = (".spec.ts", ".test.ts", ".spec.js", ".test.js")


def resolve_path(raw: str, root: Path) -> Path | None:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    try:
        return path.resolve()
    except OSError:
        return None


def find_app_root(path: Path, repo: Path) -> Path | None:
    current = path.parent
    while True:
        vitest = current / "node_modules" / ".bin" / "vitest"
        if (current / "package.json").is_file() and vitest.is_file():
            return current
        if current == repo or current.parent == current:
            return None
        current = current.parent


def spec_for(path: Path) -> Path | None:
    if path.name.endswith(SPEC_SUFFIXES):
        return path if path.is_file() else None
    for suffix in (".spec.ts", ".test.ts"):
        candidate = path.with_name(f"{path.stem}{suffix}")
        if candidate.is_file():
            return candidate
    return None


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
    if path is None or not path.is_file():
        log_hook(SCRIPT, event_name, result="skip", reason="missing_file", file=file_path)
        sys.stdout.write("{}\n")
        return 0

    spec = spec_for(path)
    app = find_app_root(path, root) if spec is not None else None
    if spec is None or app is None:
        log_hook(SCRIPT, event_name, result="skip", reason="no_sibling_spec", file=str(path))
        sys.stdout.write("{}\n")
        return 0

    vitest = app / "node_modules" / ".bin" / "vitest"
    rel = spec.relative_to(app)
    ran = subprocess.run(
        [str(vitest), "run", str(rel)],
        cwd=app,
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    output = "\n".join(part for part in (ran.stdout, ran.stderr) if part)
    summary = next(
        (line.strip() for line in reversed(output.splitlines()) if line.strip()),
        "",
    )
    log_hook(
        SCRIPT,
        event_name,
        result="ran",
        file=str(path),
        spec=str(spec),
        exit=ran.returncode,
        summary=summary[:200] or None,
    )

    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
