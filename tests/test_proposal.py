"""Check that a proposal supports the meeting decision and its claimed pilot evidence."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from proposal import render, validate


class ProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / "examples" / "aperture"
        cls.sample = json.loads((cls.folder / "proposal.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.case = copy.deepcopy(self.sample)

    def issues(self):
        return " ".join(validate(self.case, self.folder))

    def test_completed_example_and_pilot(self):
        self.assertEqual(self.issues(), "")
        self.assertIn("pilot.json", render(self.case))
        values = json.loads((self.folder / "pilot.json").read_text(encoding="utf-8"))
        fine = [row for row in values if row.get("intervals") == 128]
        self.assertEqual(len(fine), 2)
        self.assertLess(max(r["absolute_error"] for r in fine), 1e-4)
        self.assertLess(values[-1]["difference_error"], values[-1]["error_bound"])

    def test_no_observation_without_results(self):
        self.case["tests"][0]["artifact"] = "../pilot.json"
        self.assertIn("observed result", self.issues())

    def test_plans_do_not_render_observations(self):
        test = self.case["tests"][0]
        test.update(state="planned")
        self.assertIn("separate observed", self.issues())
        for key in ("artifact", "result", "measurements"):
            test.pop(key)
        self.assertEqual(self.issues(), "")
        self.assertIn("尚无观测结果", render(self.case))

    def test_simulation_only_rules_out_field_test(self):
        self.case["tests"][0]["mode"] = "field"
        self.assertIn("outside allowed modes", self.issues())

    def test_changed_display_value_is_detected(self):
        row = self.case["tests"][0]
        row["result"] = row["result"].replace("0.864679", "0.865679")
        self.assertIn("reported number differs", self.issues())

    def test_extra_digits_or_swapped_labels_are_detected(self):
        row = self.case["tests"][0]
        original = row["result"]
        row["result"] = original.replace("0.864679", "0.864679999")
        self.assertIn("reported number differs", self.issues())
        row["result"] = original.replace("0.864665", "SWAP").replace("0.864679", "0.864665").replace("SWAP", "0.864679")
        self.assertIn("reported number differs", self.issues())

    def test_does_not_accept_one_sided_or_unfalsifiable_test(self):
        row = self.case["tests"][0]
        row.update(hypotheses=["H1"], routes=["R1"], pivot=row["proceed"])
        issues = self.issues()
        for text in ("distinguish explanations", "explicit baseline", "indistinguishable"):
            self.assertIn(text, issues)

    def test_calibration_can_use_one_route_if_decisive_test_remains(self):
        aux = copy.deepcopy(self.case["tests"][0])
        aux.update(id="T2", purpose="sanity", routes=["R1"], hypotheses=["H1"])
        self.case["tests"].append(aux)
        self.assertEqual(self.issues(), "")
        self.assertIn("实现自检涉及路线 R1", render(self.case))

    def test_broken_provenance_or_orphaned_route(self):
        self.case["hypotheses"][0]["sources"] = ["missing"]
        self.case["choice"] = "R3"
        self.assertIn("unknown sources", self.issues())
        self.assertIn("chosen route", self.issues())


if __name__ == "__main__":
    unittest.main()
