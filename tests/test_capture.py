import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from capture_run import capture


class CaptureTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def run_case(self, code, timeout=5):
        (self.root / "simulate.py").write_text(code, encoding="utf-8")
        return capture(self.root, "trial", "simulate.py", [], [], timeout)

    def test_actual_result_and_no_overwriting_trial(self):
        r = self.run_case("print('[0, 1.25]')")
        self.assertEqual(r["status"], "recorded")
        saved = self.root / "runs" / "trial"
        self.assertEqual(json.loads((saved / "result.json").read_bytes()), [0, 1.25])
        self.assertEqual(json.loads((saved / "receipt.json").read_bytes())["inputs"], r["inputs"])
        with self.assertRaises(FileExistsError):
            capture(self.root, "trial", "simulate.py", [], [], 5)

    def test_failed_and_timeout_do_not_become_results(self):
        r = self.run_case("raise ArithmeticError('failed')")
        self.assertEqual(r["status"], "process_failed")
        self.assertFalse((self.root / "runs/trial/result.json").exists())
        (self.root / "simulate.py").write_text("import time; time.sleep(3)")
        r = capture(self.root, "trial-2", "simulate.py", [], [], 0.05)
        self.assertEqual(r["status"], "timeout")

    def test_invalid_numeric_output_or_mutated_input(self):
        self.assertEqual(self.run_case("print('[1e1000]')")["status"], "invalid_output_or_input")
        source = self.root / "settings"
        source.write_text("initial")
        (self.root / "simulate.py").write_text("from pathlib import Path\nPath('settings').write_text('changed')\nprint('[1]')")
        r = capture(self.root, "changed", "simulate.py", ["settings"], [], 5)
        self.assertEqual(r["status"], "invalid_output_or_input")

    def test_out_of_case_rejected(self):
        with self.assertRaises(ValueError):
            capture(self.root, "trial", "../external.py", [], [], 5)


if __name__ == "__main__":
    unittest.main()
