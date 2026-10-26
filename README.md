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

## Scope and limitations
This is an educational reference implementation, not a semantic LLM judge. Text matching does not establish correctness of meaning. No proprietary code, prompts, benchmarks, or customer data are used.

## License
MIT
