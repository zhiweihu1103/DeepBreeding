"""JSONL tagging utilities."""

from __future__ import annotations

import json
from pathlib import Path


def inject_retrieval_word(filepath: Path, keyword: str) -> None:
    """Add `retrieval_word` to every valid JSONL record in a file."""

    if not filepath.exists() or filepath.stat().st_size == 0:
        return

    with filepath.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    with filepath.open("w", encoding="utf-8") as file:
        for line in lines:
            if not line.strip():
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            data["retrieval_word"] = keyword
            file.write(json.dumps(data, ensure_ascii=False) + "\n")
