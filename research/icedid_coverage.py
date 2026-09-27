#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path(__file__).with_name("icedid_case_study.json")

TACTIC_HINTS = {
    "T1071.001": "command-and-control",
    "T1547.001": "persistence",
    "T1055.004": "defense-evasion",
    "T1055.012": "defense-evasion",
    "T1082": "discovery",
    "T1016": "discovery",
    "T1518.001": "discovery",
    "T1218.007": "defense-evasion",
    "T1218.011": "defense-evasion",
    "T1053.005": "persistence",
    "T1497": "defense-evasion",
    "T1047": "execution",
}

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def summarize(doc):
    by_tactic = {}
    for tid, name, note in doc["techniques"]:
        tactic = TACTIC_HINTS.get(tid, "other")
        by_tactic.setdefault(tactic, []).append({"id": tid, "name": name, "note": note})
    return {
        "family": doc["family"],
        "attack_id": doc["attack_id"],
        "technique_count": len(doc["techniques"]),
        "by_tactic": by_tactic,
        "research_questions": [
            "Which IcedID behaviors are observable with endpoint telemetry?",
            "Which ATT&CK behaviors have safe Atomic Red Team equivalents?",
            "Which detections remain stable when benign telemetry changes?",
            "Where are coverage gaps between behavior, telemetry, and detection?"
        ]
    }

if __name__ == "__main__":
    print(json.dumps(summarize(load()), ensure_ascii=False, indent=2))
