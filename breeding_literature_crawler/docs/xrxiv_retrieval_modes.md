# xRxiv Retrieval Modes

## Purpose

xRxiv local retrieval uses local dumps through `paperscraper` for bioRxiv, medRxiv, and chemRxiv. Candidate records can be written after source-specific relevance filtering, or they can be written directly as coarse retrieval output.

The default lab workflow keeps relevance filtering enabled. Coarse retrieval is available for exploratory use cases where users want all valid local search candidates returned by `paperscraper`.

## Default Mode: Filtered Retrieval

The recommended default is:

```yaml
biorxiv:
  enable_relevance_filter: true
```

In this mode, xRxiv local search writes candidate records to a temporary JSONL file, applies source-specific relevance filtering, and then writes retained records to the configured source output directory.

- bioRxiv uses a relaxed source-specific policy.
- medRxiv and chemRxiv use stricter policies.
- Filtering reduces clearly irrelevant cross-domain noise.
- Filtering does not guarantee a fully clean crop breeding corpus.

## Coarse Mode: Disable Filtering

For coarse bioRxiv retrieval:

```yaml
biorxiv:
  enable_relevance_filter: false
```

This writes all valid local search candidates returned by `paperscraper`. It increases recall but also increases noise.

Coarse retrieval can be useful for:

- Exploratory analysis
- Custom downstream classifiers
- Users who want to design their own filtering strategy
- Auditing the effect of the repository's default relevance filtering

Coarse output should not be treated as a curated or high-quality crop breeding corpus.

## Recommended Safe Workflow

When switching modes, use a separate output directory or intentionally regenerate existing outputs.

For example:

```yaml
biorxiv:
  output_dir: data/raw/biorxiv_coarse
  enable_relevance_filter: false
```

This avoids mixing filtered and coarse JSONL files in the same directory.

Because `skip_if_exists` may skip existing JSONL files, users should choose one of the following:

- Set a new `output_dir`, such as `data/raw/biorxiv_coarse`.
- Remove or move previous outputs before rerunning.
- Set `skip_if_exists: false` only if intentionally regenerating outputs.

Do not commit large coarse retrieval outputs or generated corpus files to the public repository.

## Command

Run the bioRxiv local retrieval entry script after editing `configs/sources.yaml`:

```powershell
.\.venv\Scripts\python.exe scripts\run_biorxiv_local.py
```

The same configuration pattern is also available for medRxiv and chemRxiv, although the default documentation focus is bioRxiv because it is the primary xRxiv source for crop-breeding literature.

## Downstream Impact

`scripts/run_cleaning.py` and `scripts/run_report.py` consume whatever raw JSONL files are placed in the configured source output directories.

Disabling relevance filtering increases downstream noise. Cleaning and deduplication can standardize fields, remove short-abstract records, merge duplicate records, and preserve `retrieval_word` values, but cleaning/deduplication does not replace relevance filtering.

## Recommendation

Keep `enable_relevance_filter: true` for the default lab workflow.

Use `enable_relevance_filter: false` only for coarse retrieval experiments where higher recall and higher noise are acceptable.
