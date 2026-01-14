import json
import sys
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "packages" / "conformance-v1" / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from conformance_v1.model import DrillResult, Report, Rule  # noqa: E402
from conformance_v1.report import report_to_json  # noqa: E402


class SchemaStableTests(unittest.TestCase):
    def test_attack_card_fields_present(self):
        rule = Rule(
            rule_id="Q3-SCHEMA-01",
            adversary_class=("External Hackers",),
            attack_vector="schema guard",
            surface="Reporting",
            severity="LOW",
            rationale="Ensure report schema stays stable.",
            detection="runtime drill",
            repro_command="",
        )
        result = DrillResult(rule_id=rule.rule_id, passed=False, evidence="test")
        report = Report(rules=(rule,), results=(result,))
        payload = json.loads(report_to_json(report))
        cards = payload.get("attack_cards")
        self.assertIsInstance(cards, list)
        self.assertEqual(len(cards), 1)
        card = cards[0]
        for key in (
            "rule_id",
            "adversary_class",
            "surface",
            "attack_vector",
            "repro_command",
            "evidence",
        ):
            self.assertIn(key, card)


if __name__ == "__main__":
    unittest.main()
