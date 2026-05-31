"""Cleaning entry script.

This script assembles raw source output directories from configuration and
delegates normalization, filtering, and deduplication to the cleaning layer.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.cleaning import clean_and_deduplicate_datasets
from agri_lit_pipeline.config import load_all_configs


def _get_source_cfg(cfg: dict, source_name: str) -> dict:
    """Return the source configuration for a named source."""

    sources_cfg = cfg["sources"]
    if "sources" in sources_cfg:
        return sources_cfg["sources"][source_name]
    return sources_cfg[source_name]


def main() -> None:
    """Run the cleaning pipeline configuration and dispatch flow."""

    cfg = load_all_configs()

    source_names = ["pubmed", "arxiv", "biorxiv", "medrxiv", "chemrxiv"]
    input_folders: list[Path] = []

    for source_name in source_names:
        source_cfg = _get_source_cfg(cfg, source_name)
        output_dir = Path(source_cfg["output_dir"])
        if not output_dir.is_absolute():
            output_dir = REPO_ROOT / output_dir
        input_folders.append(output_dir)

    pipeline_cfg = cfg["pipeline"]
    outputs_cfg = pipeline_cfg.get("outputs", {})
    cleaning_cfg = pipeline_cfg.get("cleaning", {})

    output_filepath = Path(
        outputs_cfg.get(
            "final_clean_dataset",
            "data/intermediate/master_clean_dataset/all_breeding_papers_clean.jsonl",
        )
    )
    if not output_filepath.is_absolute():
        output_filepath = REPO_ROOT / output_filepath
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    stats = clean_and_deduplicate_datasets(
        input_folders=input_folders,
        output_filepath=output_filepath,
        min_abstract_length=cleaning_cfg.get("min_abstract_length", 50),
    )

    print("\nCleaning entry script completed.")
    print(f"Output file: {stats['output_filepath']}")
    print(f"Non-empty raw lines: {stats['total_lines_seen']}")
    print(f"Parsed JSON records: {stats['total_json_loaded']}")
    print(f"Records with valid abstracts: {stats['total_records_with_valid_abstract']}")
    print(f"Duplicate records merged: {stats['duplicates_merged']}")
    print(f"Unique records saved: {stats['unique_papers_saved']}")


if __name__ == "__main__":
    main()
