# Company analysis and grading rubric — synthetic reference case

> **Independent educational demonstration.** All figures and the company are fictional, with no client filings, proprietary Handshake content, or confidential case data.

## Analyst task

You are reviewing four years of financial data for **Atlas Components**, a fictional industrial manufacturer in **GICS Industrials (20)**. Data: [synthetic_industrials.json](synthetic_industrials.json). Figures are in USD millions.

Produce an investment-committee-style **company quality assessment**, not a price target. Address:

1. What are the essential sector metrics and why?
2. What explains the apparent divergence between sales growth, profitability, and cash flow?
3. How should identified nonrecurring EBITDA items be normalized?
4. What does the trend in net debt / EBITDA imply for risk?
5. Which competing hypotheses can the data support or reject, and which require more evidence?
6. What evidence must be requested before a defensible valuation or investment decision?

**Do not fabricate price/volume splits, customer concentration, guidance, peer multiples, cost of capital, or filing-based assertions.**

## Deterministic checks (selected)

| Metric | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|
| Revenue | 160 | 175 | 202 | 225 |
| EBITDA | 28 | 32 | 33 | 30 |
| EBITDA margin | 17.50% | 18.29% | 16.34% | 13.33% |
| Operating cash flow | 23 | 30 | 24 | 16 |
| CapEx | 12 | 15 | 22 | 27 |
| Free cash flow (CFO − CapEx) | 11 | 15 | 2 | −11 |
| Net debt | 65 | 70 | 90 | 118 |
| Net debt / EBITDA | 2.32x | 2.19x | 2.73x | 3.93x |
| Operating working capital (AR + inventory − AP) | 25 | 29 | 37 | 51 |

**2025 revenue grew 11.39% year on year**, yet reported EBITDA fell **9.09%**. FY2025 operating working capital increased by **14** relative to FY2024. The dataset does not provide a complete cash-flow reconciliation, so it does **not** prove that the working-capital increase alone caused the decline in CFO.

**Nonrecurring item flags:** FY2023 EBITDA includes a fictional **+4** nonrecurring gain (normalized EBITDA **28**); FY2025 includes a fictional **−2** restructuring charge (normalized EBITDA **32**). Treat normalization as a documented adjustment, not a claim that all restructuring costs are nonrecurring in practice.

## Gold-standard reference analysis — concise

The business shows **top-line expansion but deteriorating earnings quality**. Revenue rose from 160 to 225 over four years, but EBITDA margin fell from 17.50% to 13.33%, cash flow after CapEx shifted from +11 to −11, and net leverage rose to 3.93x in FY2025. These trends justify additional diligence before applying an attractive valuation multiple.

The FY2025 restructuring adjustment lifts EBITDA to 32, but this **does not resolve weak cash conversion**. Normalized FY2025 leverage is still approximately **3.69x** (118 / 32). FY2023's gain should likewise be removed before comparing underlying profitability.

**Competing hypotheses:** Cost inflation, unfavorable product mix, pricing pressure, and capacity expansion all remain plausible. Without cost breakdowns, price/volume data, project-level CapEx detail, and customer concentration, the dataset cannot uniquely identify the root cause. Higher operating working capital and CapEx provide observable *potential* explanations for declining free cash flow, not definitive attribution.

**Recommended additional evidence:** audited annual reports and accounting notes, normalized EBITDA bridge, revenue price-volume-mix bridge, cash flow and working-capital reconciliation, maintenance versus growth CapEx, covenant terms, debt maturity schedule, customer concentration, and comparable-company valuation data.

**Committee position:** **Defer valuation judgment** until those analyses are completed. Do not assign a target price from unsupported assumptions.

## Grading rubric (100 points)

Each criterion should be scored independently against available evidence.

| ID | Weight | What a strong response must do |
|---|---:|---|
| R1 — Sector KPI selection | 15 | Select and justify industrial-sector KPIs: margins, cash conversion, capital intensity, working capital, leverage; distinguish drivers from reported outcomes. |
| R2 — Multi-year interpretation | 20 | Quantify revenue, EBITDA, margin, FCF and leverage trends accurately and explain why the combined pattern matters. |
| R3 — Accounting normalization | 15 | Remove the signed +4 gain and −2 charge correctly; separate normalized EBITDA from reported cash flow; disclose potential limits of add-backs. |
| R4 — Cash conversion and risk | 20 | Calculate CFO − CapEx, recognize higher working capital and investment needs, discuss net leverage and refinancing risk without inventing covenant breaches. |
| R5 — Hypotheses and evidence | 15 | Distinguish proven observations from plausible hypotheses; request missing price/volume, cost, CapEx, segment and peer data; avoid unsupported causation. |
| R6 — Recommendation and calibration | 15 | Provide a conditional, evidence-based investment stance, list next diligence actions, and avoid unsupported valuation precision. |
| **Total** | **100** | |

### Review guidance

- A persuasive narrative without correct calculations should **not** receive full credit.
- Do not reward guessed facts, invented regulatory/accounting treatments, unsupported price targets, or false causal claims.
- A caveat about uncertainty should receive credit only if it identifies **what is missing and why it matters**.
- If an output states that FY2025 free cash flow is positive, treat this as a **material arithmetic error**.
- The rubric requires **human judgment** for semantic criteria. Simple string matches do not establish financial correctness.

## Reproduce the calculations

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

See [finance_metrics.py](../src/llm_eval/finance_metrics.py) for deterministic metric calculations and [test_finance_metrics.py](../tests/test_finance_metrics.py) for tests.
