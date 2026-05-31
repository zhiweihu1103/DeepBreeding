"""Raw inventory report entry script.

This script assembles crop, technology, and source-output configuration, then
delegates raw inventory report generation to the reporting layer.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import get_all_crops, get_technologies, load_all_configs
from agri_lit_pipeline.reporting import generate_inventory_markdown_report


def _get_source_cfg(cfg: dict, source_name: str) -> dict:
    """Return the source configuration for a named source."""

    sources_cfg = cfg["sources"]
    if "sources" in sources_cfg:
        return sources_cfg["sources"][source_name]
    return sources_cfg[source_name]


def main() -> None:
    """Run the raw inventory reporting configuration and dispatch flow."""

    cfg = load_all_configs()
    crops = get_all_crops(cfg)
    technologies = get_technologies(cfg)

    databases: dict[str, Path] = {}
    source_labels = {
        "pubmed": "PubMed",
        "arxiv": "arXiv",
        "biorxiv": "bioRxiv",
        "medrxiv": "medRxiv",
        "chemrxiv": "chemRxiv",
    }

    for source_name, label in source_labels.items():
        source_cfg = _get_source_cfg(cfg, source_name)
        output_dir = Path(source_cfg["output_dir"])
        if not output_dir.is_absolute():
            output_dir = REPO_ROOT / output_dir
        databases[label] = output_dir

    pipeline_cfg = cfg["pipeline"]
    outputs_cfg = pipeline_cfg.get("outputs", {})

    output_filepath = Path(outputs_cfg.get("report_markdown", "docs/raw_inventory_report.md"))
    if not output_filepath.is_absolute():
        output_filepath = REPO_ROOT / output_filepath
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    stats = generate_inventory_markdown_report(
        crops=crops,
        technologies=technologies,
        databases=databases,
        output_filepath=output_filepath,
    )

    print("\nReport entry script completed.")
    print(f"Output file: {stats['output_filepath']}")
    print(f"Sources: {stats['num_sources']}")
    print(f"Crops: {stats['num_crops']}")
    print(f"Technologies: {stats['num_technologies']}")
    print(f"Raw inventory total: {stats['total_all_db']}")


if __name__ == "__main__":
    main()
