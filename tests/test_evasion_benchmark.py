import unittest
from pathlib import Path
import importlib.util

MODULE = Path(__file__).resolve().parents[1] / "research" / "evasion_benchmark.py"
spec = importlib.util.spec_from_file_location("evasion_benchmark", MODULE)
m = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(m)

class EvasionBenchmarkTests(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(m.run(2026, 120), m.run(2026, 120))

    def test_profiles_present(self):
        r = m.run(2026, 120)
        self.assertEqual([x["profile"] for x in r["results"]], ["baseline", "P1", "P2", "P3"])
        self.assertEqual(len(r["sensitivity"]), 6)

    def test_feature_bounds(self):
        for s in m.generate(1, 20):
            for value in s.features.values():
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

if __name__ == "__main__":
    unittest.main()
