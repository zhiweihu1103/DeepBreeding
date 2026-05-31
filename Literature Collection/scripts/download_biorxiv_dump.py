"""bioRxiv dump download entry script."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import load_all_configs
from agri_lit_pipeline.sources.xrxiv import download_biorxiv_dump


def main() -> None:
    """Prepare configured paths and delegate bioRxiv dump download."""

    cfg = load_all_configs()
    sources_cfg = cfg["sources"]

    if "sources" in sources_cfg:
        biorxiv_cfg = sources_cfg["sources"]["biorxiv"]
    else:
        biorxiv_cfg = sources_cfg["biorxiv"]

    if not biorxiv_cfg.get("enabled", True):
        print("bioRxiv is disabled in configuration; skipping dump download.")
        return

    dump_dir = Path(biorxiv_cfg.get("dump_dir", "data/private/server_dumps/biorxiv"))
    if not dump_dir.is_absolute():
        dump_dir = REPO_ROOT / dump_dir
    dump_dir.mkdir(parents=True, exist_ok=True)

    print("Starting bioRxiv dump download.")
    print(f"Configured dump directory: {dump_dir}")

    success = download_biorxiv_dump(
        max_retries=biorxiv_cfg.get("max_retries", 5),
        retry_sleep_seconds=biorxiv_cfg.get("retry_sleep_seconds", 10),
    )

    if success:
        print("bioRxiv dump download flow completed.")
    else:
        print("bioRxiv dump download failed; check network conditions and retry.")


if __name__ == "__main__":
    main()
