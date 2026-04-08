from __future__ import annotations

from pathlib import Path


def chunk_files(files: list[Path], chunk_size: int = 10) -> list[list[Path]]:
    if chunk_size < 8 or chunk_size > 10:
        raise ValueError("chunk_size must be between 8 and 10 for parallel processing policy")
    return [files[i : i + chunk_size] for i in range(0, len(files), chunk_size)]
