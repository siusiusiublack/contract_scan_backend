"""Source-agnostic parse helpers.

Source-specific XML handling lives on the adapter; this module holds shared text cleanup.
"""

from __future__ import annotations

import re


def collapse_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
