# Contributing

Contributions are welcome through issues, documentation updates, script improvements, and workflow refinements.

## Basic Principles

- Do not commit full raw retrieval results, full cleaned datasets, private datasets, or large intermediate files.
- Keep path and data-directory changes backward-compatible where possible.
- If output fields change, update `README.md` and `docs/dataset_schema.md`.
- Keep entry scripts thin; place reusable logic under `src/agri_lit_pipeline/`.

## Suggested Workflow

1. Create a branch from the current repository structure.
2. Make a focused code or documentation change.
3. Check `.gitignore` before committing to avoid adding `data/raw/`, `data/cleaned/`, `data/private/`, dumps, caches, or generated corpus files.
4. Record the change scope, affected scripts, and validation steps in the pull request.

## Validation

Useful lightweight checks include:

- Python compile check for `src/` and `scripts/`
- Entry script import smoke test
- MkDocs build for documentation changes
- Small private-sample validation for retrieval, cleaning, or reporting changes
