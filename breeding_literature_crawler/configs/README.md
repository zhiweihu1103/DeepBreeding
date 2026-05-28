# Configs Guide

`configs/` stores the YAML files that drive the workflow. The main design principle is to keep crop vocabularies, technology vocabularies, source parameters, and downstream pipeline settings separate from source code.

## Files

- `crops.yaml` maintains crop vocabularies, currently grouped into categories such as `staple` and `minor`.
- `technologies.yaml` maintains technology keywords, with the main workflow using the breeding-oriented technology set.
- `sources.yaml` defines source switches, modes, output directories, and execution parameters for PubMed, arXiv, bioRxiv, medRxiv, and chemRxiv.
- `pipeline.yaml` defines cross-source paths and downstream cleaning/reporting settings.

## Maintenance Notes

- Prefer changing vocabularies in YAML rather than editing entry scripts.
- Do not commit private or full-scale data outputs when testing configuration changes.
- For temporary smoke tests, use a private copy or short-lived branch with reduced vocabularies.
- Source-specific aliases and relevance filtering rules are maintained in code, not in these YAML files.
