#!/usr/bin/env python3
"""Synthetic detector-evasion benchmark for defensive research.

This module never loads, mutates, executes, or emits real payloads/binaries.
It operates only on abstract feature vectors so experiments are reproducible
without providing a path to bypass production AV/EDR.
"""
from __future__ import annotations
import argparse
import json
import math
import random
from dataclasses import dataclass, asdict
from pathlib import Path

FEATURES = ("exec_surface", "io_surface", "network_surface", "persistence_surface", "entropy", "token_overlap")
WEIGHTS = {
    "exec_surface": 1.25,
    "io_surface": 0.75,
    "network_surface": 1.10,
    "persistence_surface": 1.50,
    "entropy": 0.55,
    "token_overlap": 1.35,
}
BIAS = -2.65
THRESHOLD = 0.50

@dataclass
class Sample:
    sample_id: str
    label: int
    features: dict[str, float]

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def score(features: dict[str, float]) -> float:
    z = BIAS + sum(WEIGHTS[k] * features[k] for k in FEATURES)
    return sigmoid(z)

def detected(features: dict[str, float]) -> bool:
    return score(features) >= THRESHOLD

def clamp(v: float) -> float:
    return max(0.0, min(1.0, v))

def generate(seed: int = 2026, n: int = 240) -> list[Sample]:
    rng = random.Random(seed)
    rows: list[Sample] = []
    for i in range(n):
        label = 1 if i < n // 2 else 0
        center = 0.68 if label else 0.28
        f = {}
        for name in FEATURES:
            jitter = rng.uniform(-0.22, 0.22)
            feature_center = center
            if name == "entropy":
                feature_center += 0.08 if label else -0.02
            if name == "persistence_surface":
                feature_center += 0.10 if label else -0.06
            f[name] = clamp(feature_center + jitter)
        rows.append(Sample(f"S{i:04d}", label, f))
    return rows

def perturb(features: dict[str, float], profile: str) -> dict[str, float]:
    """Apply abstract, non-operational feature-space perturbations only."""
    f = dict(features)
    if profile == "P1":
        f["token_overlap"] = clamp(f["token_overlap"] - 0.18)
        f["entropy"] = clamp(f["entropy"] + 0.07)
    elif profile == "P2":
        f["exec_surface"] = clamp(f["exec_surface"] - 0.12)
        f["io_surface"] = clamp(f["io_surface"] - 0.10)
        f["entropy"] = clamp(f["entropy"] + 0.10)
    elif profile == "P3":
        f["token_overlap"] = clamp(f["token_overlap"] - 0.16)
        f["network_surface"] = clamp(f["network_surface"] - 0.10)
        f["persistence_surface"] = clamp(f["persistence_surface"] - 0.08)
    elif profile != "baseline":
        raise ValueError(f"unknown profile: {profile}")
    return f

def metrics(samples: list[Sample], profile: str) -> dict:
    tp = fp = tn = fn = 0
    scores: list[float] = []
    for s in samples:
        f = perturb(s.features, profile)
        pred = detected(f)
        scores.append(score(f))
        if s.label and pred: tp += 1
        elif s.label and not pred: fn += 1
        elif not s.label and pred: fp += 1
        else: tn += 1
    recall = tp / (tp + fn) if tp + fn else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {
        "profile": profile,
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "recall": round(recall, 4),
        "false_positive_rate": round(fpr, 4),
        "mean_score": round(sum(scores) / len(scores), 4),
    }

def sensitivity(samples: list[Sample]) -> list[dict]:
    out = []
    positives = [s for s in samples if s.label == 1]
    for name in FEATURES:
        changed = 0
        delta_sum = 0.0
        for s in positives:
            base = score(s.features)
            f = dict(s.features)
            f[name] = clamp(f[name] - 0.15)
            after = score(f)
            delta_sum += base - after
            changed += int(detected(s.features) and not detected(f))
        out.append({
            "feature": name,
            "mean_score_drop": round(delta_sum / max(1, len(positives)), 4),
            "decision_flips": changed,
        })
    return sorted(out, key=lambda x: (x["decision_flips"], x["mean_score_drop"]), reverse=True)

def run(seed: int, n: int) -> dict:
    samples = generate(seed, n)
    profiles = ["baseline", "P1", "P2", "P3"]
    results = [metrics(samples, p) for p in profiles]
    baseline_recall = results[0]["recall"]
    for row in results:
        row["recall_delta_vs_baseline"] = round(row["recall"] - baseline_recall, 4)
    return {
        "schema": "lr-payload-lab/synthetic-evasion-benchmark-v1",
        "seed": seed,
        "samples": n,
        "scope": "synthetic feature vectors only; no executable payloads or production AV bypass",
        "detector": {"threshold": THRESHOLD, "weights": WEIGHTS, "bias": BIAS},
        "results": results,
        "sensitivity": sensitivity(samples),
    }

def main() -> int:
    ap = argparse.ArgumentParser(description="Run the synthetic detector-evasion benchmark")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--samples", type=int, default=240)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    report = run(args.seed, args.samples)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
