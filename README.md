# Python LLM Evaluation Framework

An **original, self-contained** Python reference project demonstrating transparent, reproducible, criterion-based response evaluation. All inputs are synthetic.

## Features
- Parse evaluation cases from JSONL
- Score required text, forbidden text, and structured JSON fields
- Report per-criterion results, per-case scores, and dataset mean
- Reject malformed inputs and duplicate case IDs
- Automated unit tests with GitHub Actions

## Quick start
Requires Python 3.10+ and no external packages.

```bash
PYTHONPATH=src python -m llm_eval.cli examples/cases.jsonl --output report.json
python -m unittest discover -s tests -v
```

## JSONL format

```json
{"id":"demo","response":"The validation passed.","criteria":[{"kind":"contains","value":"passed"},{"kind":"not_contains","value":"failed"}]}
```

Kinds: `contains`, `not_contains`, `json_keys` (a list of required top-level object keys). Each criterion has equal weight. Text matching is case-insensitive. The score is the fraction passed.

## Synthetic finance company-analysis case

The repository includes an independent, fully fictional **Industrials (GICS 20)** case:
- [Four-year financial dataset](examples/synthetic_industrials.json) — revenue, EBITDA, operating cash flow, CapEx, net debt and working capital.
- [Investment committee case, reference answer and 100-point evaluation rubric](examples/company_analysis_and_rubric.md).
- [Deterministic company metrics](src/llm_eval/finance_metrics.py) with [unit tests](tests/test_finance_metrics.py).

The case illustrates sector KPI selection, earnings normalization, multi-year trends, cash conversion, leverage and evidence-aware reasoning. All figures are synthetic. The rubric is designed for expert review; deterministic arithmetic is tested separately from qualitative judgments.

## Scope and limitations
This is an educational reference implementation, not a semantic LLM judge. Text matching does not establish correctness of meaning. No proprietary code, prompts, benchmarks, or customer data are used.

## License
MIT
