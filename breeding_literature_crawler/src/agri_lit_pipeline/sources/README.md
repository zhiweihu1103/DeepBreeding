# Sources Layer Guide

`sources/` contains source-specific retrieval implementations. This layer keeps the real differences among scholarly sources explicit instead of forcing all sources into one opaque interface.

## Current Files

- `pubmed.py` handles PubMed online retrieval using query pairs.
- `arxiv.py` handles arXiv online retrieval and source-specific query string construction.
- `xrxiv.py` handles shared dump download and local search behavior for bioRxiv, medRxiv, and chemRxiv.

## Design Principles

- The query builder produces structured `(crop, technology)` pairs.
- Source-specific query conversion stays in the source layer.
- xRxiv relevance filtering stays close to xRxiv local search behavior.

## Maintenance Areas

The most likely future changes are in `xrxiv.py` and `relevance.py`, especially around bioRxiv relevance filtering. Changes should remain small, inspectable, and source-specific.
