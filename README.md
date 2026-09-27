# LR-PayloadLab

<p align="center"><img src="./docs/media/social-preview.svg" alt="LR-PayloadLab" width="100%"></p>
<p align="center"><img src="./docs/media/demo.gif" alt="LR-PayloadLab reproducible demo" width="100%"></p>
<p align="center"><strong>Payload telemetry × Detection evasion research × Reproducible experiments.</strong></p>
<p align="center">把“载荷是否能被检测、检测为什么失效、怎样加固检测器”做成一套可复现实验链。</p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/LR-PayloadLab/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Research" src="https://img.shields.io/badge/research-detection%20resilience-8b5cf6"></p>

## 30 秒看懂

LR-PayloadLab 现在包含两条研究链：

```text
Track A
Manifest → Policy validation → Bounded execution → Receipt → Rollback

Track B
Synthetic Sample → Explainable Detector → Feature Perturbation
               → Recall / FPR / Decision Flip → Sensitivity Analysis
```

Track A 用来生成可审计、可回滚的无害遥测场景；Track B 用来研究“检测器面对载荷特征变化时为什么会漏报”。

## 载荷实验

```bash
python -m pip install -e .
payload-lab plan examples/telemetry-demo.json
payload-lab run examples/telemetry-demo.json --receipt receipt.json
payload-lab rollback receipt.json
payload-lab build examples/telemetry-demo.json --output generated-payload.py
```

示例只产生临时标记、无害子进程、文件哈希、短时计算与延迟，并记录 SHA-256 和逐动作回执。

## Detection Evasion Benchmark

```bash
python research/evasion_benchmark.py
python research/evasion_benchmark.py --samples 1000 --json report.json
```

这部分用于导师展示“免杀/检测对抗”研究方法，但实验对象是 **合成特征向量**，不会生成或修改真实恶意程序，也不会调用生产环境 AV/EDR。

输出包括：

- baseline / P1 / P2 / P3 的 TP、FN、FP、TN
- Recall / False Positive Rate
- 相比 baseline 的 recall delta
- 特征敏感度与 decision flips
- 固定 seed 的可复现实验结果

详细设计见 [Detection Evasion Study](./docs/detection-evasion-study.md)。

## 研究价值

- **可审计 Payload**：Manifest 完整描述实验行为，执行结果有回执。
- **检测对抗评估**：不只展示“能不能检出”，还量化检测率随特征扰动如何变化。
- **可解释性**：直接输出哪些特征最容易导致 decision flip。
- **可复现性**：固定模型、固定随机种子、自动化测试。
- **安全边界**：不包含真实 AV/EDR 绕过、注入、持久化、凭据访问或隐蔽远控能力。

## 导师展示路线

建议现场只演示三步：

```text
1. 运行 benign payload，展示 receipt / rollback
2. 运行 detection-evasion benchmark，展示 recall 下降
3. 打开 sensitivity 结果，解释“检测器为什么漏、应该怎么加固”
```

这比单纯做一个“免杀程序”更适合研究型项目：既能体现攻防思维，也能留下完整实验方法、指标和代码证据。

作者：LLR6 · MIT License
