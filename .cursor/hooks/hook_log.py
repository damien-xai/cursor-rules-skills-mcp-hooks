"""Append one record to .cursor/logs/hooks.log and hooks.jsonl. Fail open.

Never pass secret values, prompt text, or raw hook payloads into `data`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def log_hook(script: str, event: str, **data: object) -> None:
	try:
		log_dir = Path.cwd() / ".cursor" / "logs"
		log_dir.mkdir(parents=True, exist_ok=True)
		logged_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
		record = {"logged_at": logged_at, "script": script, "event": event, **data}
		with (log_dir / "hooks.jsonl").open("a", encoding="utf-8") as handle:
			handle.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
		extras = "  ".join(f"{key}={value}" for key, value in data.items() if value is not None)
		line = f"{logged_at}  {event}  {script}"
		if extras:
			line = f"{line}  {extras}"
		with (log_dir / "hooks.log").open("a", encoding="utf-8") as handle:
			handle.write(line + "\n")
	except OSError:
		return
