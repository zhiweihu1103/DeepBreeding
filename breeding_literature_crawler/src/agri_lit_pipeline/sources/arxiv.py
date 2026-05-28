"""arXiv source layer."""

from __future__ import annotations

import time
from pathlib import Path

from paperscraper.arxiv import get_and_dump_arxiv_papers

from agri_lit_pipeline.tagging import inject_retrieval_word


def crawl_arxiv_pairs(
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    sleep_seconds: int = 5,
    max_retries: int = 3,
    skip_if_exists: bool = True,
    rate_limit_sleep_seconds: int = 60,
    network_retry_sleep_seconds: int = 15,
) -> None:
    """Run arXiv retrieval and tag successful JSONL outputs.

    arXiv uses a stricter source-specific query string to reduce noisy matches.
    """

    for crop, tech in query_pairs:
        keyword = f"{crop} {tech}"
        save_name = keyword.lower().replace(" ", "_") + ".jsonl"
        save_path = output_root_path / save_name

        if skip_if_exists and save_path.exists() and save_path.stat().st_size > 10:
            print(f"[{save_name}] exists; skipping arXiv retrieval.")
            continue

        query_str_strict = f'{crop} "{tech}"'
        query = [[query_str_strict]]

        for attempt in range(max_retries):
            try:
                print(
                    f"Searching arXiv: {query_str_strict} "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )

                get_and_dump_arxiv_papers(query, output_filepath=str(save_path))

                if save_path.exists() and save_path.stat().st_size > 10:
                    inject_retrieval_word(save_path, keyword)
                    print(f"Retrieved and tagged arXiv output: {save_name}")
                else:
                    if save_path.exists():
                        save_path.unlink()
                    print(f"No arXiv records retained for: {save_name}")

                time.sleep(sleep_seconds)
                break

            except KeyboardInterrupt:
                print("Interrupted by user; exiting safely.")
                raise
            except Exception as exc:
                error_msg = str(exc)
                print(
                    f"arXiv retrieval failed for [{keyword}] / "
                    f"strict query [{query_str_strict}]: {error_msg}"
                )

                if save_path.exists() and save_path.stat().st_size == 0:
                    save_path.unlink()

                if attempt == max_retries - 1:
                    print(f"[{save_name}] reached max retries; skipping.")
                    break

                if "HTTP 429" in error_msg:
                    print(
                        f"Rate limit detected; sleeping {rate_limit_sleep_seconds} "
                        "seconds before retry."
                    )
                    time.sleep(rate_limit_sleep_seconds)
                else:
                    print(
                        f"Non-429 error; sleeping {network_retry_sleep_seconds} "
                        "seconds before retry."
                    )
                    time.sleep(network_retry_sleep_seconds)
