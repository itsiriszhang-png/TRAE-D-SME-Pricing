import unittest

from agentic_ai.reasoner import run_trae_for_sme


class TestReasoner(unittest.TestCase):
    def test_standard_profile_baseline(self):
        result = run_trae_for_sme("GBA_Eco_Standard", "Baseline")

        self.assertIn("score", result)
        self.assertIn("pricing", result)
        self.assertIn("explanation", result)

        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

        pricing = result["pricing"]
        self.assertIn(pricing["risk_grade"], ["A", "B", "C", "D"])
        self.assertIn("Prime +", pricing["base_rate_str"])

    def test_highrisk_triggers_review(self):
        result = run_trae_for_sme("GBA_Eco_HighRisk", "Compliance Risk")
        self.assertTrue(result["pricing"]["need_manual_review"])


if __name__ == "__main__":
    unittest.main()
