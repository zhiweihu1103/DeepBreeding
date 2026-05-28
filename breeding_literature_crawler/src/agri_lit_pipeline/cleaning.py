"""Multi-source JSONL cleaning and deduplication."""

from __future__ import annotations

import json
from pathlib import Path

from agri_lit_pipeline.normalize import normalize_doi, normalize_title


def _coerce_retrieval_words(value: object) -> list[str]:
    """Normalize a `retrieval_word` value into `list[str]`."""

    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [value] if value.strip() else []
    if value is None:
        return []
    return [str(value)] if str(value).strip() else []


def clean_and_deduplicate_datasets(
    input_folders: list[Path],
    output_filepath: Path,
    min_abstract_length: int = 50,
) -> dict:
    """Clean raw JSONL records, deduplicate them, and write a master JSONL file.

    The current deduplication policy prioritizes normalized DOI values and falls
    back to normalized titles when DOI is unavailable. Duplicate records merge
    their `retrieval_word` values so query pair traceability is preserved.
    """

    unique_papers_dict: dict[str, dict] = {}

    total_lines_seen = 0
    total_json_loaded = 0
    total_records_with_valid_abstract = 0
    duplicates_merged = 0

    print("Starting cleaning pipeline: normalize, filter, and deduplicate JSONL records.")
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    for folder in input_folders:
        if not folder.exists():
            print(f"Warning: input directory does not exist; skipped: {folder}")
            continue

        print(f"Processing directory: {folder}")

        for filepath in folder.iterdir():
            if not filepath.is_file() or filepath.suffix.lower() != ".jsonl":
                continue

            with filepath.open("r", encoding="utf-8") as input_file:
                for line in input_file:
                    if not line.strip():
                        continue

                    total_lines_seen += 1

                    try:
                        paper = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    total_json_loaded += 1

                    abstract = paper.get("abstract")
                    if not (
                        abstract
                        and isinstance(abstract, str)
                        and len(abstract.strip()) > min_abstract_length
                    ):
                        continue

                    total_records_with_valid_abstract += 1

                    clean_doi = normalize_doi(paper.get("doi"))
                    clean_title = normalize_title(paper.get("title"))

                    identifier = clean_doi if clean_doi else clean_title
                    if not identifier:
                        continue

                    new_retrieval_words = _coerce_retrieval_words(paper.get("retrieval_word"))

                    if identifier in unique_papers_dict:
                        duplicates_merged += 1
                        existing_paper = unique_papers_dict[identifier]
                        existing_words = _coerce_retrieval_words(
                            existing_paper.get("retrieval_word")
                        )

                        for word in new_retrieval_words:
                            if word not in existing_words:
                                existing_words.append(word)

                        existing_paper["retrieval_word"] = existing_words
                    else:
                        paper["retrieval_word"] = new_retrieval_words
                        unique_papers_dict[identifier] = paper

    with output_filepath.open("w", encoding="utf-8") as output_file:
        for paper in unique_papers_dict.values():
            output_file.write(json.dumps(paper, ensure_ascii=False) + "\n")

    unique_papers_saved = len(unique_papers_dict)
    stats = {
        "total_lines_seen": total_lines_seen,
        "total_json_loaded": total_json_loaded,
        "total_records_with_valid_abstract": total_records_with_valid_abstract,
        "duplicates_merged": duplicates_merged,
        "unique_papers_saved": unique_papers_saved,
        "output_filepath": output_filepath,
    }

    print("\n" + "=" * 50)
    print("Cleaning pipeline completed.")
    print(f"Non-empty raw lines: {total_lines_seen}")
    print(f"Parsed JSON records: {total_json_loaded}")
    print(f"Records with valid abstracts: {total_records_with_valid_abstract}")
    print(f"Duplicate records merged: {duplicates_merged}")
    print(f"Unique records saved: {unique_papers_saved}")
    print(f"Output file: {output_filepath}")
    print("=" * 50 + "\n")

    return stats
