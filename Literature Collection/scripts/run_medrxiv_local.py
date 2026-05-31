"""medRxiv local dump search entry script."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import get_all_crops, get_technologies, load_all_configs
from agri_lit_pipeline.query_builder import build_crop_tech_pairs
from agri_lit_pipeline.sources.xrxiv import crawl_medrxiv_pairs


def main() -> None:
    """Run configured medRxiv local dump search."""

    cfg = load_all_configs()
    all_crops = get_all_crops(cfg)
    technologies = get_technologies(cfg)
    sources_cfg = cfg["sources"]

    if "sources" in sources_cfg:
        medrxiv_cfg = sources_cfg["sources"]["medrxiv"]
    else:
        medrxiv_cfg = sources_cfg["medrxiv"]

    if not medrxiv_cfg.get("enabled", True):
        print("medRxiv is disabled in configuration; skipping local search.")
        return

    output_root_path = Path(medrxiv_cfg["output_dir"])
    if not output_root_path.is_absolute():
        output_root_path = REPO_ROOT / output_root_path
    output_root_path.mkdir(parents=True, exist_ok=True)

    query_pairs = build_crop_tech_pairs(all_crops, technologies)
    print(f"Generated {len(query_pairs)} medRxiv local-search query pairs.")

    crawl_medrxiv_pairs(
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        skip_if_exists=medrxiv_cfg.get("skip_if_exists", True),
        enable_relevance_filter=medrxiv_cfg.get("enable_relevance_filter", True),
    )


if __name__ == "__main__":
    main()
