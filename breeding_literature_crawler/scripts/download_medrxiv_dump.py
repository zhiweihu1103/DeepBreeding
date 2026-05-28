"""medRxiv dump download entry script."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import load_all_configs
from agri_lit_pipeline.sources.xrxiv import download_medrxiv_dump


def main() -> None:
    """Prepare configured paths and delegate medRxiv dump download."""

    cfg = load_all_configs()
    sources_cfg = cfg["sources"]

    if "sources" in sources_cfg:
        medrxiv_cfg = sources_cfg["sources"]["medrxiv"]
    else:
        medrxiv_cfg = sources_cfg["medrxiv"]

    if not medrxiv_cfg.get("enabled", True):
        print("medRxiv is disabled in configuration; skipping dump download.")
        return

    dump_dir = Path(medrxiv_cfg.get("dump_dir", "data/private/server_dumps/medrxiv"))
    if not dump_dir.is_absolute():
        dump_dir = REPO_ROOT / dump_dir
    dump_dir.mkdir(parents=True, exist_ok=True)

    print("Starting medRxiv dump download.")
    print(f"Configured dump directory: {dump_dir}")

    success = download_medrxiv_dump(
        max_retries=medrxiv_cfg.get("max_retries", 5),
        retry_sleep_seconds=medrxiv_cfg.get("retry_sleep_seconds", 10),
    )

    if success:
        print("medRxiv dump download flow completed.")
    else:
        print("medRxiv dump download failed; check network conditions and retry.")


if __name__ == "__main__":
    main()
