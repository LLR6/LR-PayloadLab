# Detection Evasion Study — Safe Research Track

这个实验用于展示 **“检测器在输入特征发生扰动后是否仍然稳定”**，而不是提供真实杀软绕过能力。

## 研究问题

1. 一个检测器过度依赖哪些特征？
2. 当这些特征发生小幅变化时，召回率下降多少？
3. 哪些扰动最容易造成 decision flip？
4. 如何通过特征多样化、阈值校准与规则组合提高鲁棒性？

## 实验设计

`research/evasion_benchmark.py` 只生成合成特征向量，不读取 PE/ELF，不执行载荷，也不调用 Defender/EDR。

每个样本由 6 个抽象维度组成：

- `exec_surface`
- `io_surface`
- `network_surface`
- `persistence_surface`
- `entropy`
- `token_overlap`

检测器是固定权重的可解释模型。P1/P2/P3 是 **纯特征空间扰动**，不对应真实混淆、注入、打包或规避技术。

## 运行

```bash
python research/evasion_benchmark.py
python research/evasion_benchmark.py --samples 1000 --json report.json
```

输出包括：

- baseline / P1 / P2 / P3 的 TP、FN、FP、TN
- Recall 与 False Positive Rate
- 相比 baseline 的 recall delta
- 每个特征的平均分数下降和 decision flips

## 导师展示建议

把重点放在 **“为什么检测器漏掉了”** 和 **“怎么把它修好”**：

```text
Synthetic Sample
      ↓
Explainable Detector
      ↓
Feature-space Perturbation
      ↓
Recall / FPR / Decision Flip
      ↓
Sensitivity Analysis
      ↓
Detector Hardening
```

这条路线能体现检测对抗、实验设计、指标评估和可解释性，同时不会把仓库变成真实 AV/EDR 规避工具。
