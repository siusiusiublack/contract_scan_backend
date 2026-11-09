"""Fill shared document schema + housing practice_area tags."""

from __future__ import annotations

import re

HOUSING_KEYWORDS = (
    "tenancy",
    "tenant",
    "landlord",
    "assured shorthold",
    "deposit",
    "possession",
    "housing act",
    "rent repayment",
    "disrepair",
    "guarantor",
    "section 21",
    "section 8",
)


def make_doc_id(source: str, uri: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9._/-]+", "_", uri.strip("/"))
    return f"{source}:{safe}"


def assign_practice_areas(title: str, text: str) -> list[str]:
    blob = f"{title}\n{text}".lower()
    if any(k in blob for k in HOUSING_KEYWORDS):
        return ["housing"]
    return ["unclassified"]


def is_housing_relevant(title: str, text: str) -> bool:
    return "housing" in assign_practice_areas(title, text)
