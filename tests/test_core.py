import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from llm_eval.core import EvaluationError, evaluate_case, evaluate_dataset


class EvaluationTests(unittest.TestCase):
    def test_full_score(self):
        case = {"id": "one", "response": "SUCCESS",
                "criteria": [{"kind": "contains", "value": "success"},
                             {"kind": "not_contains", "value": "failure"}]}
        self.assertEqual(evaluate_case(case)["score"], 1.0)

    def test_partial_score(self):
        case = {"id": "two", "response": "alpha",
                "criteria": [{"kind": "contains", "value": "alpha"},
                             {"kind": "contains", "value": "beta"}]}
        self.assertEqual(evaluate_case(case)["score"], 0.5)

    def test_json_keys(self):
        case = {"id": "three", "response": json.dumps({"ok": True}),
                "criteria": [{"kind": "json_keys", "value": ["ok"]}]}
        self.assertTrue(evaluate_case(case)["passed"])

    def test_json_array_not_object(self):
        case = {"id": "array", "response": '["ok"]',
                "criteria": [{"kind": "json_keys", "value": ["ok"]}]}
        self.assertFalse(evaluate_case(case)["passed"])

    def test_invalid_kind(self):
        with self.assertRaises(EvaluationError):
            evaluate_case({"id": "x", "response": "ok",
                           "criteria": [{"kind": "unsupported", "value": "ok"}]})

    def test_duplicate_ids(self):
        case = {"id": "x", "response": "ok",
                "criteria": [{"kind": "contains", "value": "ok"}]}
        with self.assertRaises(EvaluationError):
            evaluate_dataset([case, case])

    def test_empty_dataset(self):
        with self.assertRaises(EvaluationError):
            evaluate_dataset([])


if __name__ == "__main__":
    unittest.main()
