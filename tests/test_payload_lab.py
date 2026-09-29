import json,tempfile,unittest
from pathlib import Path
from payload_lab.cli import build,execute,manifest_digest,rollback,validate

MANIFEST={"schema":"lr-payload-lab/v1","name":"test","actions":[{"type":"write_marker","path":"x/a.txt","content":"ok"},{"type":"spawn_echo","text":"hello"},{"type":"hash_file","path":"x/a.txt"}]}
class PayloadTests(unittest.TestCase):
 def test_run_receipt_and_rollback(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r=execute(MANIFEST,root);self.assertTrue((root/"x/a.txt").exists());self.assertEqual(r["events"][1]["stdout"],"hello");self.assertEqual(r["manifest_sha256"],manifest_digest(MANIFEST));rollback(r,root);self.assertFalse((root/"x/a.txt").exists())
 def test_escape_and_unknown_action_rejected(self):
  with self.assertRaises(ValueError):validate({"schema":"lr-payload-lab/v1","actions":[{"type":"write_marker","path":"../x"}]})
  with self.assertRaises(ValueError):validate({"schema":"lr-payload-lab/v1","actions":[{"type":"network_connect"}]})
 def test_build_is_auditable(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"payload.py";sha=build(MANIFEST,p);self.assertEqual(len(sha),64);self.assertIn("MANIFEST",p.read_text())
 def test_manifest_digest_is_canonical(self):
  reordered={"name":"test","actions":MANIFEST["actions"],"schema":"lr-payload-lab/v1"}
  self.assertEqual(manifest_digest(MANIFEST),manifest_digest(reordered))
  self.assertEqual(len(manifest_digest(MANIFEST)),64)
if __name__=="__main__":unittest.main()
