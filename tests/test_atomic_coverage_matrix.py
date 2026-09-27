import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "research" / "atomic_coverage_matrix.py"
spec = importlib.util.spec_from_file_location("atomic_coverage_matrix", P)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

class AtomicCoverageMatrixTests(unittest.TestCase):
    def setUp(self):
        self.mapping = m.load_json(ROOT / "research" / "atomic_coverage_map.json")

    def test_mapping_counts(self):
        report = m.build_report(self.mapping)
        self.assertEqual(report["summary"]["ttp_total"], 12)
        self.assertEqual(report["summary"]["exact_atomic_mappings"], 11)
        self.assertEqual(report["summary"]["no_exact_atomic"], 1)

    def test_default_is_not_run(self):
        report = m.build_report(self.mapping)
        self.assertTrue(all(x["run_status"] == "not_run" for x in report["rows"]))
        self.assertEqual(report["summary"]["detections_evaluated"], 0)

    def test_real_result_merge(self):
        first = self.mapping["mappings"][0]
        results = {
            "schema": "lr-payload-lab/atomic-results-v1",
            "results": [{
                "technique_id": first["technique_id"],
                "atomic_guid": first["atomic_guid"],
                "run_status": "passed",
                "detection": "detected",
                "telemetry": ["example-log"]
            }]
        }
        report = m.build_report(self.mapping, results)
        self.assertEqual(report["summary"]["experiments_recorded"], 1)
        self.assertEqual(report["summary"]["detected"], 1)

    def test_unknown_result_rejected(self):
        results = {
            "schema": "lr-payload-lab/atomic-results-v1",
            "results": [{
                "technique_id": "T0000",
                "atomic_guid": None,
                "run_status": "passed",
                "detection": "detected"
            }]
        }
        with self.assertRaises(ValueError):
            m.build_report(self.mapping, results)

if __name__ == "__main__":
    unittest.main()
