#!/usr/bin/env python3
"""Backward-compatible entry: same checks as block-secrets.py."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("block-secrets.py")), run_name="__main__")
