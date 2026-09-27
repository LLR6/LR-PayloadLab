#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_MAP = HERE / "atomic_coverage_map.json"
RUN_STATES = {"not_run", "passed", "failed", "skipped"}
DETECTION_STATES = {"not_evaluated", "detected", "missed", "partial"}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_results(doc, mapping):
    if doc.get("schema") != "lr-payload-lab/atomic-results-v1":
        raise ValueError("unsupported results schema")
    known = {(x["technique_id"], x.get("atomic_guid")) for x in mapping["mappings"]}
    seen = set()
    for i, row in enumerate(doc.get("results", [])):
        key = (row.get("technique_id"), row.get("atomic_guid"))
        if key in seen:
            raise ValueError(f"duplicate result at index {i}: {key}")
        seen.add(key)
        if key not in known:
            raise ValueError(f"unknown technique/guid pair at index {i}: {key}")
        if row.get("run_status", "not_run") not in RUN_STATES:
            raise ValueError(f"invalid run_status at index {i}")
        if row.get("detection", "not_evaluated") not in DETECTION_STATES:
            raise ValueError(f"invalid detection at index {i}")
    return doc

def build_report(mapping, results=None):
    result_by_key = {}
    if results:
        validate_results(results, mapping)
        result_by_key = {(x["technique_id"], x.get("atomic_guid")): x for x in results.get("results", [])}

    rows = []
    for item in mapping["mappings"]:
        key = (item["technique_id"], item.get("atomic_guid"))
        observed = result_by_key.get(key, {})
        rows.append({
            **item,
            "run_status": observed.get("run_status", "not_run"),
            "detection": observed.get("detection", "not_evaluated"),
            "telemetry": observed.get("telemetry", []),
            "evidence": observed.get("evidence", ""),
            "notes": observed.get("notes", item.get("note", "")),
        })

    exact = sum(1 for x in rows if x["exact_atomic"])
    run = sum(1 for x in rows if x["run_status"] != "not_run")
    evaluated = [x for x in rows if x["detection"] != "not_evaluated"]
    detected = sum(1 for x in evaluated if x["detection"] == "detected")
    missed = sum(1 for x in evaluated if x["detection"] == "missed")
    partial = sum(1 for x in evaluated if x["detection"] == "partial")

    return {
        "schema": "lr-payload-lab/atomic-coverage-report-v1",
        "threat_model": mapping["threat_model"],
        "summary": {
            "ttp_total": len(rows),
            "exact_atomic_mappings": exact,
            "no_exact_atomic": len(rows) - exact,
            "experiments_recorded": run,
            "detections_evaluated": len(evaluated),
            "detected": detected,
            "missed": missed,
            "partial": partial,
        },
        "rows": rows,
    }

def render_markdown(report):
    s = report["summary"]
    lines = [
        "# IcedID Atomic Coverage Matrix",
        "",
        f"- Threat model: **{report['threat_model']['family']} ({report['threat_model']['attack_id']})**",
        f"- TTPs in study: **{s['ttp_total']}**",
        f"- Exact Atomic mappings: **{s['exact_atomic_mappings']}**",
        f"- No exact Atomic mapping: **{s['no_exact_atomic']}**",
        f"- Experiments recorded: **{s['experiments_recorded']}**",
        f"- Detections evaluated: **{s['detections_evaluated']}**",
        "",
        "| ATT&CK | Atomic test | Policy | Run | Detection | Telemetry |",
        "|---|---|---|---|---|---|",
    ]
    for row in report["rows"]:
        atomic = row["atomic_name"] or "No exact parent-level Atomic"
        telemetry = ", ".join(row["telemetry"]) if row["telemetry"] else "-"
        lines.append(
            f"| {row['technique_id']} | {atomic} | {row['execution_policy']} | "
            f"{row['run_status']} | {row['detection']} | {telemetry} |"
        )
    lines += [
        "",
        "## Reading the matrix",
        "",
        "- metadata-only: mapped for research and coverage analysis, but this project does not provide an execution wrapper.",
        "- isolated-lab: suitable for an authorized isolated test host after reviewing upstream prerequisites and cleanup.",
        "- needs-representative-subtechnique: parent ATT&CK technique without an exact parent-level Atomic test.",
        "- not_run / not_evaluated: no experimental claim is being made yet.",
        "",
        "This report records evidence; it does not execute Atomic Red Team tests.",
    ]
    return "\n".join(lines) + "\n"

def main():
    ap = argparse.ArgumentParser(description="Build an IcedID ATT&CK / Atomic Red Team coverage matrix")
    ap.add_argument("--map", type=Path, default=DEFAULT_MAP)
    ap.add_argument("--results", type=Path)
    ap.add_argument("--markdown", type=Path)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    mapping = load_json(args.map)
    results = load_json(args.results) if args.results else None
    report = build_report(mapping, results)
    if args.markdown:
        args.markdown.write_text(render_markdown(report), encoding="utf-8")
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
