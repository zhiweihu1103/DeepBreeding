"""PubMed entry script.

This script loads configuration, builds crop-technology query pairs, normalizes
the output directory, and delegates PubMed retrieval to the source layer.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

# Support direct execution with `python scripts/run_pubmed.py` without requiring
# the package to be installed first.
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import get_all_crops, get_technologies, load_all_configs
from agri_lit_pipeline.query_builder import build_crop_tech_pairs
from agri_lit_pipeline.sources.pubmed import crawl_pubmed_pairs


def main() -> None:
    """Run the PubMed configuration and retrieval dispatch flow."""

    cfg = load_all_configs()
    all_crops = get_all_crops(cfg)
    technologies = get_technologies(cfg)

    sources_cfg = cfg["sources"]
    if "sources" in sources_cfg:
        pubmed_cfg = sources_cfg["sources"]["pubmed"]
    else:
        pubmed_cfg = sources_cfg["pubmed"]

    if not pubmed_cfg.get("enabled", True):
        print("PubMed is disabled in configuration; skipping retrieval.")
        return

    output_root_path = Path(pubmed_cfg["output_dir"])
    if not output_root_path.is_absolute():
        output_root_path = REPO_ROOT / output_root_path
    output_root_path.mkdir(parents=True, exist_ok=True)

    query_pairs = build_crop_tech_pairs(all_crops, technologies)
    print(f"Generated {len(query_pairs)} PubMed query pairs.")

    crawl_pubmed_pairs(
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        sleep_seconds=pubmed_cfg.get("sleep_seconds", 2),
    )


if __name__ == "__main__":
    main()
