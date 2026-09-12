#!/usr/bin/env python3
"""afterMCPExecution hook: log MCP tool request + response for tail -f."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from hook_log import log_hook


def parse_maybe_json(value):
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return value
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return value
    return value


def dump(value) -> str:
    if value is None:
        return "(none)"
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, ensure_ascii=False, default=str)


def main() -> int:
    raw = sys.stdin.read()
    root = Path.cwd()
    log_dir = root / ".cursor" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {"_unparsed": raw}

    if not isinstance(payload, dict):
        payload = {"_value": payload}

    logged_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    event = payload.get("hook_event_name") or "afterMCPExecution"
    tool = payload.get("tool_name") or payload.get("tool") or "(unknown tool)"
    duration = payload.get("duration")
    request = parse_maybe_json(payload.get("tool_input", payload.get("arguments")))
    response = parse_maybe_json(payload.get("result_json", payload.get("result")))

    record = {
        "logged_at": logged_at,
        "event": event,
        "tool_name": tool,
        "duration_ms": duration,
        "conversation_id": payload.get("conversation_id"),
        "generation_id": payload.get("generation_id"),
        "request": request,
        "response": response,
    }

    jsonl_path = log_dir / "mcp.jsonl"
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    duration_label = f"{duration}ms" if duration is not None else "duration n/a"
    block = "\n".join(
        [
            f"======== {logged_at}  {event}  {duration_label} ========",
            f"tool: {tool}",
            "-- request --",
            dump(request),
            "-- response --",
            dump(response),
            "",
        ]
    )
    pretty_path = log_dir / "mcp.log"
    with pretty_path.open("a", encoding="utf-8") as handle:
        handle.write(block + "\n")

    log_hook("log-mcp", event, result="logged", tool=tool, duration_ms=duration)

    # afterMCPExecution is fire-and-forget; empty JSON is enough.
    sys.stdout.write("{}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
