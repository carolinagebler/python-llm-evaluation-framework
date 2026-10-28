"""Synthetic company-analysis metrics; educational reference, not investment advice.

This module intentionally performs only deterministic calculations.
It does not infer whether a company is investable or judge semantic correctness.
"""
from __future__ import annotations

from typing import Any


def analyze_years(years: list[dict[str, Any]]) -> list[dict[str, float | int | None]]:
    """Compute comparable company metrics for sorted, consecutive annual observations."""
    if not isinstance(years, list) or len(years) < 2:
        raise ValueError("At least two annual observations are required.")
    required = {"year", "revenue", "ebitda", "operating_cash_flow",
                "capex", "net_debt", "receivables", "inventory", "payables"}
    output: list[dict[str, float | int | None]] = []
    previous: dict[str, Any] | None = None
    seen: set[int] = set()
    for item in years:
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValueError("Missing required financial fields.")
        year = item["year"]
        if type(year) is not int or year in seen:
            raise ValueError("Years must be unique integers.")
        if previous is not None and year != previous["year"] + 1:
            raise ValueError("Observations must be consecutive and ascending.")
        seen.add(year)
        fields = required - {"year"}
        if any(type(item[field]) not in (int, float) for field in fields):
            raise ValueError("All financial values must be numeric.")
        if item["revenue"] <= 0 or item["ebitda"] <= 0:
            raise ValueError("Revenue and EBITDA must be positive.")
        nwc = item["receivables"] + item["inventory"] - item["payables"]
        prior_nwc = (previous["receivables"] + previous["inventory"] -
                     previous["payables"]) if previous else None
        output.append({
            "year": year,
            "revenue_growth_pct": round(
                (item["revenue"] / previous["revenue"] - 1) * 100, 2
            ) if previous else None,
            "ebitda_margin_pct": round(item["ebitda"] / item["revenue"] * 100, 2),
            "free_cash_flow": round(item["operating_cash_flow"] - item["capex"], 2),
            "fcf_to_ebitda_pct": round(
                (item["operating_cash_flow"] - item["capex"]) / item["ebitda"] * 100, 2
            ),
            "net_debt_to_ebitda": round(item["net_debt"] / item["ebitda"], 2),
            "operating_nwc": round(nwc, 2),
            "change_in_operating_nwc": round(nwc - prior_nwc, 2)
            if previous else None,
        })
        previous = item
    return output


def normalized_ebitda(reported_ebitda: float, one_off_effect: float) -> float:
    """Remove the signed EBITDA impact of an identified nonrecurring item.

    E.g. a +4 gain is subtracted; a -2 charge is added back.
    Adjustments need independent accounting justification.
    """
    return reported_ebitda - one_off_effect
