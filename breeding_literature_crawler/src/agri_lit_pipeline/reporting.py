"""Raw inventory report generation."""

from __future__ import annotations

from pathlib import Path


def _count_non_empty_lines(filepath: Path) -> int:
    """Count non-empty lines in a JSONL file."""

    with filepath.open("r", encoding="utf-8") as input_file:
        return sum(1 for line in input_file if line.strip())


def generate_inventory_markdown_report(
    crops: list[str],
    technologies: list[str],
    databases: dict[str, Path],
    output_filepath: Path,
) -> dict:
    """Generate a crop-by-technology-by-source raw inventory report.

    The report counts raw JSONL records. It is not a cleaned corpus size or a
    final data quality evaluation.
    """

    db_keys = list(databases.keys())
    header = (
        f"| Crop | Technology | {' | '.join(db_keys)} | **Raw Retrieval Total** |"
    )
    separator = "|" + "|".join(["---"] * (len(db_keys) + 3)) + "|"

    report_lines = [header, separator]
    total_all_db = 0

    print("Generating raw inventory report...\n")

    for crop in crops:
        for tech in technologies:
            keyword = f"{crop} {tech}"
            filename = keyword.lower().replace(" ", "_") + ".jsonl"

            row_data = [crop.title(), tech]
            row_total = 0

            for db_name, folder_path in databases.items():
                filepath = folder_path / filename
                count = _count_non_empty_lines(filepath) if filepath.exists() else 0
                row_data.append(str(count) if count > 0 else "-")
                row_total += count

            row_data.append(f"**{row_total}**")
            total_all_db += row_total
            report_lines.append(f"| {' | '.join(row_data)} |")

    summary_text = (
        "\n\n### Raw Inventory Summary\n"
        f"This raw inventory covers {len(crops)} crops, {len(technologies)} "
        f"technologies, and {len(databases)} sources. Raw retrieval total: "
        f"{total_all_db} non-empty records."
    )
    report_lines.append(summary_text)

    output_filepath.parent.mkdir(parents=True, exist_ok=True)
    with output_filepath.open("w", encoding="utf-8") as output_file:
        output_file.write("\n".join(report_lines))

    print("Raw inventory report completed.")
    print(f"Output file: {output_filepath}")
    print(f"Raw inventory total: {total_all_db}")

    return {
        "total_all_db": total_all_db,
        "output_filepath": output_filepath,
        "num_crops": len(crops),
        "num_technologies": len(technologies),
        "num_sources": len(databases),
    }
