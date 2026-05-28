# bioRxiv Relevance Filtering Review Template

Use this template after small changes to bioRxiv relevance filtering rules. The goal is to judge whether a change reduces obvious cross-domain noise without removing too many agricultural breeding records.

This template is intended for bioRxiv review only. medRxiv and chemRxiv are treated more conservatively because their candidate results are noisier for agricultural breeding use cases.

## Run Context

- Review date:
- Code version or branch:
- Entry script: `scripts/run_biorxiv_local.py`
- Rule change under review:

Example rule changes:

- Add a crop scientific-name alias.
- Add a conservative technology synonym.
- Remove an overly broad relaxed signal.

## Log Summary

Review three to five representative query pairs. Prefer a mix of:

1. A query pair with many `missing crop token` failures
2. A query pair with many `missing tech token` failures
3. A query pair with a moderate pass rate
4. A query pair important to the current research question

Suggested examples:

- `rice_gwas`
- `maize_marker-assisted_selection`
- `wheat_genomic_selection`
- `rice_qtl_mapping`
- `maize_germplasm`

| Query | Candidate records | Passed | Filtered | Pass rate | Main failure reason |
| --- | ---: | ---: | ---: | ---: | --- |
| `rice_gwas` |  |  |  |  |  |
| `maize_marker-assisted_selection` |  |  |  |  |  |
| `wheat_genomic_selection` |  |  |  |  |  |
| `...` |  |  |  |  |  |

```text
pass rate = passed records / candidate records
```

## Review Questions

### Crop Constraint

If `missing crop token` remains high, inspect whether candidates are mostly technology-only hits without a clear crop context. For bioRxiv, the crop signal should remain a meaningful gate.

### Technology Constraint

If `missing tech token` is high but manual review finds many clearly relevant agricultural breeding papers, consider whether a conservative technology synonym should be added.

### Strict and Relaxed Signals

Track whether strict technology tokens still account for most retained records. Relaxed signals should supplement strict matching, not dominate it.

## Passed Sample Review

For each representative query, sample around 10 passed records.

| Sample | Title | Clearly relevant? | Reason | Keep under current rule? |
| --- | --- | --- | --- | --- |
| 1 |  | yes / no / borderline |  | keep / uncertain |
| 2 |  | yes / no / borderline |  | keep / uncertain |
| 3 |  | yes / no / borderline |  | keep / uncertain |
| 4 |  | yes / no / borderline |  | keep / uncertain |
| 5 |  | yes / no / borderline |  | keep / uncertain |

Summary:

- Clearly relevant count:
- Borderline count:
- Obvious noise count:
- Initial judgment: good enough / too loose / too strict

## Filtered Sample Review

For each representative query, sample around 10 filtered records.

| Sample | Title | Actually relevant? | Current failure reason | False negative? |
| --- | --- | --- | --- | --- |
| 1 |  | yes / no / borderline | missing crop / missing tech | yes / no |
| 2 |  | yes / no / borderline | missing crop / missing tech | yes / no |
| 3 |  | yes / no / borderline | missing crop / missing tech | yes / no |
| 4 |  | yes / no / borderline | missing crop / missing tech | yes / no |
| 5 |  | yes / no / borderline | missing crop / missing tech | yes / no |

Summary:

- Correctly filtered count:
- Borderline count:
- False negative count:
- Initial judgment: reasonable / slightly strict / clearly too strict

## Decision

One-sentence summary:

- Current bioRxiv filter state: too strict / acceptable / too loose

Recommendation:

- Keep the rule unchanged.
- Add a small crop alias.
- Add a small technology signal.
- Remove or narrow an overly broad relaxed signal.

Specific follow-up:

- Keep:
- Add:
- Remove:
- Defer:
