import importlib.util
import sys
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research" / "icedid_coverage.py"
spec = importlib.util.spec_from_file_location("icedid_coverage", P)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

class IcedIDCoverageTests(unittest.TestCase):
    def test_case_study_shape(self):
        d = m.load()
        self.assertEqual(d["attack_id"], "S0483")
        self.assertEqual(d["platform"], "Windows")
        self.assertGreaterEqual(len(d["techniques"]), 10)

    def test_summary_groups(self):
        s = m.summarize(m.load())
        self.assertIn("discovery", s["by_tactic"])
        self.assertIn("defense-evasion", s["by_tactic"])
        self.assertEqual(s["technique_count"], 12)

if __name__ == "__main__":
    unittest.main()
