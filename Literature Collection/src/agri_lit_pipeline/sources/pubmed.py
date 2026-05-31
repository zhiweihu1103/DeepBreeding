"""PubMed source layer."""

from __future__ import annotations

import time
from pathlib import Path

from paperscraper.pubmed import get_and_dump_pubmed_papers

from agri_lit_pipeline.tagging import inject_retrieval_word


def crawl_pubmed_pairs(
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    sleep_seconds: int = 2,
    skip_if_exists: bool = True,
) -> None:
    """Run PubMed retrieval and tag successful JSONL outputs."""

    for crop, tech in query_pairs:
        keyword = f"{crop} {tech}"
        save_name = keyword.lower().replace(" ", "_") + ".jsonl"
        save_path = output_root_path / save_name

        if skip_if_exists and save_path.exists() and save_path.stat().st_size > 10:
            print(f"[{save_name}] exists; skipping PubMed retrieval.")
            continue

        query = [[crop, tech]]

        try:
            print(f"Searching PubMed: {keyword} ...")
            get_and_dump_pubmed_papers(query, output_filepath=str(save_path))

            inject_retrieval_word(save_path, keyword)
            print(f"Retrieved and tagged PubMed output: {save_name}")

            time.sleep(sleep_seconds)

        except KeyboardInterrupt:
            print("Interrupted by user; exiting safely.")
            raise
        except Exception as exc:
            print(f"PubMed retrieval failed for [{keyword}]: {exc}")

            if save_path.exists() and save_path.stat().st_size == 0:
                save_path.unlink()
