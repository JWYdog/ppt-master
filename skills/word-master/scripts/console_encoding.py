#!/usr/bin/env python3
"""
Word Master - Console Encoding

Configure directly runnable tools to emit UTF-8 safely on Windows terminals.

Usage:
    Import configure_utf8_stdio from a Word Master CLI entry point.

Examples:
    from console_encoding import configure_utf8_stdio

Dependencies:
    None (only uses the standard library).
"""

import sys


def configure_utf8_stdio() -> None:
    """Configure stdout and stderr for UTF-8 when the runtime supports it."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            reconfigure(encoding="utf-8", errors="replace")
