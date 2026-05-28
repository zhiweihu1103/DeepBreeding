"""arXiv entry script.

This script loads configuration, builds crop-technology query pairs, normalizes
the output directory, and delegates arXiv retrieval to the source layer. The
source layer owns arXiv-specific query string construction.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import get_all_crops, get_technologies, load_all_configs
from agri_lit_pipeline.query_builder import build_crop_tech_pairs
from agri_lit_pipeline.sources.arxiv import crawl_arxiv_pairs


def main() -> None:
    """Run the arXiv configuration and retrieval dispatch flow."""

    cfg = load_all_configs()
    all_crops = get_all_crops(cfg)
    technologies = get_technologies(cfg)

    sources_cfg = cfg["sources"]
    if "sources" in sources_cfg:
        arxiv_cfg = sources_cfg["sources"]["arxiv"]
    else:
        arxiv_cfg = sources_cfg["arxiv"]

    if not arxiv_cfg.get("enabled", True):
        print("arXiv is disabled in configuration; skipping retrieval.")
        return

    output_root_path = Path(arxiv_cfg["output_dir"])
    if not output_root_path.is_absolute():
        output_root_path = REPO_ROOT / output_root_path
    output_root_path.mkdir(parents=True, exist_ok=True)

    query_pairs = build_crop_tech_pairs(all_crops, technologies)
    print(f"Generated {len(query_pairs)} arXiv query pairs.")

    crawl_arxiv_pairs(
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        sleep_seconds=arxiv_cfg.get("sleep_seconds", 5),
        max_retries=arxiv_cfg.get("max_retries", 3),
        skip_if_exists=arxiv_cfg.get("skip_if_exists", True),
        rate_limit_sleep_seconds=arxiv_cfg.get("rate_limit_sleep_seconds", 60),
        network_retry_sleep_seconds=arxiv_cfg.get("network_retry_sleep_seconds", 15),
    )


if __name__ == "__main__":
    main()
