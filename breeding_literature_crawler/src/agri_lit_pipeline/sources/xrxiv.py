"""Shared source layer for bioRxiv, medRxiv, and chemRxiv workflows."""

from __future__ import annotations

import json
import os
import time
from collections import Counter
from pathlib import Path
from typing import Callable

from paperscraper.get_dumps import biorxiv as download_biorxiv_callable
from paperscraper.get_dumps import chemrxiv as download_chemrxiv_callable
from paperscraper.get_dumps import medrxiv as download_medrxiv_callable

from agri_lit_pipeline.relevance import (
    get_matched_crop_alias_for_paper,
    get_xrxiv_filter_mode,
    is_relevant_xrxiv_record,
)
from agri_lit_pipeline.tagging import inject_retrieval_word


def _truncate_title_for_log(title: str | None, limit: int = 90) -> str:
    """Shorten a record title for compact console logs."""

    if not title:
        return "<no title>"

    compact_title = " ".join(str(title).split())
    if len(compact_title) <= limit:
        return compact_title
    return compact_title[: limit - 3] + "..."


def _format_biorxiv_sample_log(
    paper: dict,
    crop: str,
    source_name: str,
    reason: str | None = None,
) -> str:
    """Format a bioRxiv sample title and matched crop alias for debug logs."""

    title = _truncate_title_for_log(paper.get("title"))
    matched_crop_alias = get_matched_crop_alias_for_paper(paper, crop, source_name)

    if reason is None:
        if matched_crop_alias:
            return f"{title} [crop alias: {matched_crop_alias}]"
        return title

    if matched_crop_alias:
        return f"{title} [{reason}; crop alias: {matched_crop_alias}]"
    return f"{title} [{reason}]"


def _disable_proxy_env_for_direct_download() -> None:
    """Clear common proxy environment variables before dump download."""

    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    os.environ["no_proxy"] = "*"


def download_dump_with_retry(
    source_name: str,
    download_callable: Callable[[], object],
    max_retries: int = 3,
    retry_sleep_seconds: int = 5,
) -> bool:
    """Download an xRxiv dump with bounded retry handling."""

    _disable_proxy_env_for_direct_download()

    for attempt in range(max_retries):
        try:
            print(f"Downloading {source_name} dump (attempt {attempt + 1}/{max_retries})...")
            start_time = time.time()
            download_callable()
            duration = time.time() - start_time
            print(f"{source_name} dump download succeeded in {duration:.2f} seconds.")
            return True
        except KeyboardInterrupt:
            print("Interrupted by user; exiting safely.")
            raise
        except Exception as exc:
            print(f"{source_name} dump download failed: {exc}")

            if attempt == max_retries - 1:
                break

            wait_time = retry_sleep_seconds * (attempt + 1)
            print(f"Waiting {wait_time} seconds before retrying {source_name} dump download...")
            time.sleep(wait_time)

    print(f"{source_name} dump download failed after all retries.")
    return False


def download_biorxiv_dump(
    max_retries: int = 3,
    retry_sleep_seconds: int = 5,
) -> bool:
    """Download the bioRxiv dump."""

    return download_dump_with_retry(
        source_name="bioRxiv",
        download_callable=download_biorxiv_callable,
        max_retries=max_retries,
        retry_sleep_seconds=retry_sleep_seconds,
    )


def download_medrxiv_dump(
    max_retries: int = 3,
    retry_sleep_seconds: int = 5,
) -> bool:
    """Download the medRxiv dump."""

    return download_dump_with_retry(
        source_name="medRxiv",
        download_callable=download_medrxiv_callable,
        max_retries=max_retries,
        retry_sleep_seconds=retry_sleep_seconds,
    )


def download_chemrxiv_dump(
    max_retries: int = 3,
    retry_sleep_seconds: int = 5,
) -> bool:
    """Download the chemRxiv dump."""

    return download_dump_with_retry(
        source_name="chemRxiv",
        download_callable=download_chemrxiv_callable,
        max_retries=max_retries,
        retry_sleep_seconds=retry_sleep_seconds,
    )


def crawl_local_dump_pairs(
    source_key: str,
    source_name: str,
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    skip_if_exists: bool = True,
    enable_relevance_filter: bool = True,
) -> None:
    """Run local dump search for an xRxiv source.

    Candidate records are first written by `paperscraper` to a temporary JSONL
    file. The source layer then applies the current source-specific relevance
    policy before writing the final JSONL file and adding `retrieval_word`.
    """

    # Delay this import so dump-download-only commands do not load local dumps.
    from paperscraper.load_dumps import QUERY_FN_DICT

    print(f"{source_name} local search is ready; processing query pairs...")

    if source_key not in QUERY_FN_DICT:
        print(
            f"No local search entry was found for {source_name}. Confirm that the "
            "dump is available and that paperscraper loaded it successfully."
        )
        return

    filter_mode = get_xrxiv_filter_mode(source_key)
    print(f"{source_name} relevance filtering policy: {filter_mode}.")

    for crop, tech in query_pairs:
        keyword = f"{crop} {tech}"
        save_name = keyword.lower().replace(" ", "_") + ".jsonl"
        save_path = output_root_path / save_name
        temp_path = save_path.with_suffix(".tmp.jsonl")

        if skip_if_exists and save_path.exists() and save_path.stat().st_size > 10:
            print(f"[{save_name}] exists; skipping local search.")
            continue

        query = [[crop, tech]]

        try:
            if temp_path.exists():
                temp_path.unlink()

            QUERY_FN_DICT[source_key](query, output_filepath=str(temp_path))

            if not temp_path.exists():
                print(f"{source_name} did not return a candidate file; skipped: {save_name}")
                continue

            if temp_path.stat().st_size == 0:
                temp_path.unlink()
                print(f"{source_name} returned no candidates; skipped: {save_name}")
                continue

            candidate_valid_json = 0
            passed_records = 0
            passed_reason_counter: Counter[str] = Counter()
            reason_counter: Counter[str] = Counter()
            passed_title_samples: list[str] = []
            filtered_title_samples: list[str] = []

            with temp_path.open("r", encoding="utf-8") as temp_file, save_path.open(
                "w", encoding="utf-8"
            ) as final_file:
                for line in temp_file:
                    if not line.strip():
                        continue

                    try:
                        paper = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    candidate_valid_json += 1

                    if enable_relevance_filter:
                        is_relevant, reason = is_relevant_xrxiv_record(
                            paper=paper,
                            crop=crop,
                            tech=tech,
                            source_name=source_key,
                        )
                    else:
                        is_relevant, reason = True, "filter disabled"

                    if is_relevant:
                        final_file.write(json.dumps(paper, ensure_ascii=False) + "\n")
                        passed_records += 1
                        passed_reason_counter[reason] += 1
                        if source_key == "biorxiv" and len(passed_title_samples) < 2:
                            passed_title_samples.append(
                                _format_biorxiv_sample_log(
                                    paper=paper,
                                    crop=crop,
                                    source_name=source_key,
                                )
                            )
                    else:
                        reason_counter[reason] += 1
                        if source_key == "biorxiv" and len(filtered_title_samples) < 2:
                            filtered_title_samples.append(
                                _format_biorxiv_sample_log(
                                    paper=paper,
                                    crop=crop,
                                    source_name=source_key,
                                    reason=reason,
                                )
                            )

            if temp_path.exists():
                temp_path.unlink()

            filtered_records = candidate_valid_json - passed_records

            if not save_path.exists() or save_path.stat().st_size == 0:
                if save_path.exists():
                    save_path.unlink()
                print(f"{source_name} records did not pass relevance filtering: {save_name}")
                print(
                    f"Policy: {filter_mode}; candidates: {candidate_valid_json}; "
                    f"passed: 0; filtered: {filtered_records}"
                )
                if reason_counter:
                    print(f"Filter reasons: {dict(reason_counter)}")
                if source_key == "biorxiv":
                    print(f"CURRENT_QUERY={keyword}")
                    if passed_title_samples:
                        print(f"Passed sample titles: {passed_title_samples}")
                    if filtered_title_samples:
                        print(f"Filtered sample titles: {filtered_title_samples}")
                continue

            inject_retrieval_word(save_path, keyword)
            print(f"{source_name} records retained and tagged: {save_name}")
            print(
                f"Policy: {filter_mode}; candidates: {candidate_valid_json}; "
                f"passed: {passed_records}; filtered: {filtered_records}"
            )
            if passed_reason_counter:
                print(f"Pass reason counts: {dict(passed_reason_counter)}")
            if reason_counter:
                print(f"Filter reasons: {dict(reason_counter)}")
            if source_key == "biorxiv":
                print(f"CURRENT_QUERY={keyword}")
                if passed_title_samples:
                    print(f"Passed sample titles: {passed_title_samples}")
                if filtered_title_samples:
                    print(f"Filtered sample titles: {filtered_title_samples}")
        except KeyboardInterrupt:
            print("Interrupted by user; exiting safely.")
            raise
        except Exception as exc:
            print(f"{source_name} local search failed for [{keyword}]: {exc}")

            if temp_path.exists():
                temp_path.unlink()
            if save_path.exists() and save_path.stat().st_size == 0:
                save_path.unlink()


def crawl_biorxiv_pairs(
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    skip_if_exists: bool = True,
    enable_relevance_filter: bool = True,
) -> None:
    """Run bioRxiv local dump search."""

    crawl_local_dump_pairs(
        source_key="biorxiv",
        source_name="bioRxiv",
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        skip_if_exists=skip_if_exists,
        enable_relevance_filter=enable_relevance_filter,
    )


def crawl_medrxiv_pairs(
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    skip_if_exists: bool = True,
    enable_relevance_filter: bool = True,
) -> None:
    """Run medRxiv local dump search."""

    crawl_local_dump_pairs(
        source_key="medrxiv",
        source_name="medRxiv",
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        skip_if_exists=skip_if_exists,
        enable_relevance_filter=enable_relevance_filter,
    )


def crawl_chemrxiv_pairs(
    query_pairs: list[tuple[str, str]],
    output_root_path: Path,
    skip_if_exists: bool = True,
    enable_relevance_filter: bool = True,
) -> None:
    """Run chemRxiv local dump search."""

    crawl_local_dump_pairs(
        source_key="chemrxiv",
        source_name="chemRxiv",
        query_pairs=query_pairs,
        output_root_path=output_root_path,
        skip_if_exists=skip_if_exists,
        enable_relevance_filter=enable_relevance_filter,
    )
