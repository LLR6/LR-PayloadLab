import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "samples" / "trojan_sim"
spec = importlib.util.spec_from_file_location("trojan_agent", ROOT / "agent.py")
assert spec and spec.loader
agent = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = agent
spec.loader.exec_module(agent)

class TrojanSimTests(unittest.TestCase):
    def test_loopback_only(self):
        self.assertTrue(agent.is_loopback("127.0.0.1"))
        self.assertFalse(agent.is_loopback("8.8.8.8"))

    def test_allowlist(self):
        result, should_exit = agent.handle({"cmd":"PING"})
        self.assertTrue(result["ok"])
        self.assertFalse(should_exit)

        result, _ = agent.handle({"cmd":"SHELL", "text":"whoami"})
        self.assertFalse(result["ok"])

    def test_signed_round_trip(self):
        data = {"cmd":"ECHO","text":"demo"}
        self.assertEqual(agent.unpack(agent.pack(data)), data)

if __name__ == "__main__":
    unittest.main()
