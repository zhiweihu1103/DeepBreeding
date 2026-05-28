# Dataset Schema

This document describes the most stable JSONL fields used by the pipeline. Different sources may return additional source-specific fields, but downstream processing should at least expect the fields below when they are available.

## Core Fields

| Field | Type | Description |
| --- | --- | --- |
| `title` | `string` | Literature record title |
| `abstract` | `string` | Abstract text |
| `doi` | `string` | DOI, empty when unavailable |
| `authors` | `array[string]` or `array[object]` | Author information; structure may vary by source |
| `source` | `string` | Source identifier, such as `pubmed`, `arxiv`, or `biorxiv` |
| `retrieval_word` | `string` or `array[string]` | Query pair context that retrieved the record |
| `published_date` | `string` | Publication or release date, format depending on source |

## Raw and Cleaned Stage Conventions

- Raw retrieval usually preserves source-provided fields and adds `retrieval_word`.
- Cleaning focuses on `title`, `abstract`, `doi`, and `retrieval_word` for standardization and deduplication.
- If the same paper is retrieved by multiple query pairs, `retrieval_word` may become an array after deduplication.

## Minimal Example

```json
{
  "title": "Genome-wide association study for rice drought tolerance",
  "abstract": "This record shows the expected minimal JSONL schema for the public sample set.",
  "doi": "10.0000/example-doi",
  "authors": ["Example Author", "Second Author"],
  "source": "pubmed",
  "retrieval_word": ["rice GWAS"],
  "published_date": "2025-06-10"
}
```

## Compatibility Notes

Sources may include additional fields such as `journal`, `url`, `pmid`, or `entry_id`. The public sample data demonstrates structure only and should not be treated as a complete production field inventory.
