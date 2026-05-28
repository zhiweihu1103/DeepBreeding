"""chemRxiv dump download entry script."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from agri_lit_pipeline.config import load_all_configs
from agri_lit_pipeline.sources.xrxiv import download_chemrxiv_dump


def main() -> None:
    """Prepare configured paths and delegate chemRxiv dump download."""

    cfg = load_all_configs()
    sources_cfg = cfg["sources"]

    if "sources" in sources_cfg:
        chemrxiv_cfg = sources_cfg["sources"]["chemrxiv"]
    else:
        chemrxiv_cfg = sources_cfg["chemrxiv"]

    if not chemrxiv_cfg.get("enabled", True):
        print("chemRxiv is disabled in configuration; skipping dump download.")
        return

    dump_dir = Path(chemrxiv_cfg.get("dump_dir", "data/private/server_dumps/chemrxiv"))
    if not dump_dir.is_absolute():
        dump_dir = REPO_ROOT / dump_dir
    dump_dir.mkdir(parents=True, exist_ok=True)

    print("Starting chemRxiv dump download.")
    print(f"Configured dump directory: {dump_dir}")

    success = download_chemrxiv_dump(
        max_retries=chemrxiv_cfg.get("max_retries", 5),
        retry_sleep_seconds=chemrxiv_cfg.get("retry_sleep_seconds", 10),
    )

    if success:
        print("chemRxiv dump download flow completed.")
    else:
        print("chemRxiv dump download failed; check network conditions and retry.")


if __name__ == "__main__":
    main()
