"""Command-line interface for JSONL response evaluation."""

import argparse
import json
import sys
from pathlib import Path

from .core import EvaluationError, evaluate_dataset


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate synthetic response cases")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        cases = []
        for line_no, line in enumerate(args.input.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    cases.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise EvaluationError(f"Invalid JSON at line {line_no}") from exc
        report = evaluate_dataset(cases)
        text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0
    except (EvaluationError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
