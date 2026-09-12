#!/usr/bin/env python3
"""Block .env paths and credential-like strings. Fail open on parse errors."""

from __future__ import annotations

import json
import re
import sys

from hook_log import log_hook

SCRIPT = "block-secrets"

ALLOWED_ENV_SUFFIXES = (".env.example", ".env.test")
PATH_KEYS = {"path", "file_path", "filepath", "filePath", "target_file", "targetFile"}
PLACEHOLDER = re.compile(
    r"example|placeholder|changeme|change-me|your[-_ ]|xxx+|dummy|fake|test|fixme",
    re.I,
)
ENV_TOKEN = re.compile(r"(?:^|[\s'\"`=])(?P<path>(?:[\w./-]+/)?\.env(?:\.[A-Za-z0-9_-]+)?)")
SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(
        r"(?:api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]",
        re.I,
    ),
)

MSG = "Blocked a credential-like secret or .env path. Use placeholders and .env.example."


def is_env_path(value: str) -> bool:
    normalized = value.replace("\\", "/").rstrip("/")
    name = normalized.rsplit("/", 1)[-1]
    if name.endswith(ALLOWED_ENV_SUFFIXES):
        return False
    return name == ".env" or name.startswith(".env.")


def collect_paths(node, found: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in PATH_KEYS and isinstance(value, str):
                found.append(value)
            collect_paths(value, found)
    elif isinstance(node, list):
        for item in node:
            collect_paths(item, found)


def collect_strings(node, found: list[str]) -> None:
    if isinstance(node, dict):
        for value in node.values():
            collect_strings(value, found)
    elif isinstance(node, list):
        for item in node:
            collect_strings(item, found)
    elif isinstance(node, str) and len(node) >= 8:
        found.append(node)


def looks_like_secret(text: str) -> bool:
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            if not PLACEHOLDER.search(match.group(0)):
                return True
    return False


def event_name(payload: dict) -> str:
    name = payload.get("hook_event_name")
    if isinstance(name, str) and name:
        return name
    if "prompt" in payload and "command" not in payload:
        return "beforeSubmitPrompt"
    return ""


def reply(deny: bool, event: str) -> dict:
    if event == "beforeSubmitPrompt":
        if deny:
            return {"continue": False, "user_message": MSG}
        return {"continue": True}
    if deny:
        return {"permission": "deny", "user_message": MSG, "agent_message": MSG}
    return {"permission": "allow"}


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        log_hook(SCRIPT, "unknown", result="skip", reason="invalid_json")
        sys.stdout.write("{}\n")
        return 0

    if not isinstance(payload, dict):
        log_hook(SCRIPT, "unknown", result="skip", reason="invalid_payload")
        sys.stdout.write("{}\n")
        return 0

    event = event_name(payload)
    paths: list[str] = []
    collect_paths(payload, paths)
    command = payload.get("command")
    if isinstance(command, str):
        paths.extend(match.group("path") for match in ENV_TOKEN.finditer(command))

    texts: list[str] = []
    collect_strings(payload, texts)

    env_hit = any(is_env_path(path) for path in paths)
    secret_hit = any(looks_like_secret(text) for text in texts)
    deny = env_hit or secret_hit
    if deny:
        reason = "env_path" if env_hit else "credential_pattern"
    else:
        reason = "allow"
    log_hook(SCRIPT, event or "unknown", result="deny" if deny else "allow", reason=reason)
    sys.stdout.write(json.dumps(reply(deny, event)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
