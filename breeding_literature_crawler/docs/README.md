# Docs Guide

`docs/` contains manually written public documentation and a small generated-report area for the `DeepBreeding/breeding_literature_crawler/` module. Treat this directory as an explanation layer, not as a storage location for business data or private corpora.

## Recommended Reading Order

1. [../README.md](../README.md)
2. [architecture.md](architecture.md)
3. [pipeline_overview.md](pipeline_overview.md)
4. [configuration.md](configuration.md)
5. [scripts_guide.md](scripts_guide.md)
6. [xrxiv_retrieval_modes.md](xrxiv_retrieval_modes.md)
7. [versioning.md](versioning.md)
8. [developer_notes.md](developer_notes.md)
9. [known_limitations.md](known_limitations.md)
10. [smoke_test.md](smoke_test.md)

## Document Roles

- [architecture.md](architecture.md) explains the overall architecture, layers, and data flow.
- [project_structure.md](project_structure.md) explains module folders and Git tracking boundaries.
- [configuration.md](configuration.md) explains how the four YAML configuration files drive the workflow.
- [pipeline_overview.md](pipeline_overview.md) describes the end-to-end stages from configuration to reporting.
- [scripts_guide.md](scripts_guide.md) describes major entry scripts and typical commands.
- [xrxiv_retrieval_modes.md](xrxiv_retrieval_modes.md) explains filtered and coarse xRxiv local retrieval modes.
- [developer_notes.md](developer_notes.md) records engineering decisions and maintenance boundaries.
- [versioning.md](versioning.md) explains the current module version, versioning policy, and data-versioning boundary.
- [known_limitations.md](known_limitations.md) summarizes current limitations and expected future refinement areas.
- [smoke_test.md](smoke_test.md) provides local checks that do not trigger full crawling.
- [dataset_schema.md](dataset_schema.md) documents stable JSONL fields used by raw and cleaned stages.
- [biorxiv_relevance_review_template.md](biorxiv_relevance_review_template.md) provides a manual review template for bioRxiv relevance-filtering changes.

## Generated Reports

Files under `docs/generated/` are script-generated runtime reports. They should not be treated as manually curated documentation or as final cleaned corpus quality evaluations.

## MkDocs

The repository root includes `mkdocs.yml`. To preview the documentation site locally:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

The documentation home page is [index.md](index.md).
