"""Reproducible rubric-based response scoring."""

import json


class EvaluationError(ValueError):
    """Raised when an evaluation case is invalid."""


def evaluate_case(case):
    """Evaluate a case with equal-weighted, explicit criteria."""
    if not isinstance(case, dict):
        raise EvaluationError("Case must be a JSON object")
    identifier = case.get("id")
    response = case.get("response")
    criteria = case.get("criteria")
    if not isinstance(identifier, str) or not identifier.strip():
        raise EvaluationError("Case id must be a nonempty string")
    if not isinstance(response, str):
        raise EvaluationError("Response must be a string")
    if not isinstance(criteria, list) or not criteria:
        raise EvaluationError("Criteria must be a nonempty list")

    details = []
    for criterion in criteria:
        if not isinstance(criterion, dict):
            raise EvaluationError("Criterion must be an object")
        kind, value = criterion.get("kind"), criterion.get("value")
        if kind in ("contains", "not_contains"):
            if not isinstance(value, str) or not value:
                raise EvaluationError("Text criterion requires nonempty string value")
            has_text = value.casefold() in response.casefold()
            passed = has_text if kind == "contains" else not has_text
        elif kind == "json_keys":
            if (not isinstance(value, list) or not value or
                    any(not isinstance(key, str) or not key for key in value)):
                raise EvaluationError("json_keys requires nonempty list of strings")
            try:
                obj = json.loads(response)
            except json.JSONDecodeError:
                obj = None
            passed = isinstance(obj, dict) and all(key in obj for key in value)
        else:
            raise EvaluationError(f"Unsupported criterion: {kind!r}")
        details.append({"kind": kind, "value": value, "passed": passed})

    score = sum(item["passed"] for item in details) / len(details)
    return {"id": identifier, "score": score, "passed": score == 1.0, "criteria": details}


def evaluate_dataset(cases):
    """Evaluate a nonempty dataset with unique IDs."""
    if not isinstance(cases, list) or not cases:
        raise EvaluationError("Dataset must be a nonempty list")
    results = [evaluate_case(case) for case in cases]
    ids = [result["id"] for result in results]
    if len(ids) != len(set(ids)):
        raise EvaluationError("Duplicate case IDs")
    return {
        "count": len(results),
        "mean_score": sum(result["score"] for result in results) / len(results),
        "all_passed": all(result["passed"] for result in results),
        "results": results,
    }
