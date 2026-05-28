# Configuration Guide

The workflow is configuration-driven. Four YAML files are loaded through `config.py`:

- `configs/crops.yaml`
- `configs/technologies.yaml`
- `configs/sources.yaml`
- `configs/pipeline.yaml`

This documentation explains the files without changing their business values.

## `configs/crops.yaml`

`crops.yaml` maintains crop vocabularies. The current structure separates crops into groups such as `staple` and `minor`.

Entry scripts use helper functions to merge the configured crop groups into the crop list used for query pair generation. Crop aliases and source-specific relevance rules are not configured here; those belong to source-specific logic and relevance filtering code.

## `configs/technologies.yaml`

`technologies.yaml` maintains technology keywords. The main workflow currently uses the breeding-oriented technology set, such as `breeding_core`.

Additional categories may exist as future extension points or compatibility placeholders. They should not be assumed to drive the main workflow unless the entry scripts and helper functions explicitly read them.

## `configs/sources.yaml`

`sources.yaml` describes source-level behavior for:

- `pubmed`
- `arxiv`
- `biorxiv`
- `medrxiv`
- `chemrxiv`

Common fields include:

| Field | Meaning |
| --- | --- |
| `enabled` | Whether the source is enabled |
| `mode` | Retrieval mode, such as `api` or `local_dump` |
| `output_dir` | Raw JSONL output directory |
| `dump_dir` | Declared local dump directory for xRxiv workflows |
| `skip_if_exists` | Whether to skip an output file if it already exists |
| `sleep_seconds` | Basic delay for online retrieval |
| `max_retries` | Retry count |
| `enable_relevance_filter` | Whether xRxiv relevance filtering is enabled |

Some scripts still preserve compatibility handling for older nested source structures, but the current repository uses the flat source configuration shape.

## `configs/pipeline.yaml`

`pipeline.yaml` describes downstream paths and pipeline-level parameters. Important fields include:

- `paths.*`
- `outputs.final_clean_dataset`
- `outputs.report_markdown`
- `cleaning.min_abstract_length`

`run_cleaning.py` reads the configured final cleaned dataset path. `run_report.py` reads the configured raw inventory report path.

## How Configuration Enters the Workflow

1. An entry script calls `load_all_configs()`.
2. `config.py` loads the four YAML files.
3. Helper functions produce crop and technology lists.
4. `query_builder.py` creates `(crop, technology)` query pairs.
5. Source modules translate those pairs into source-specific retrieval behavior.
6. Downstream scripts read configured output paths for cleaning and reporting.

The goal is to keep vocabularies and paths configurable while preserving source-specific retrieval and relevance filtering in code where behavior is easier to inspect and test.
