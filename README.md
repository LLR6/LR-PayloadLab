# LR-PayloadLab

<p align="center"><img src="./docs/media/social-preview.svg" alt="LR-PayloadLab" width="100%"></p>
<p align="center"><img src="./docs/media/demo.gif" alt="LR-PayloadLab reproducible demo" width="100%"></p>
<p align="center"><strong>Bounded payloads. Verifiable research.</strong></p>
<p align="center">Auditable endpoint telemetry scenarios with receipts and rollback.</p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/LR-PayloadLab/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-8b5cf6"></p>

## 30 秒看懂

用 JSON 描述研究行为，平台先检查动作白名单、路径边界和资源上限，再执行并生成逐动作回执。`rollback` 根据回执清理实验文件。

```text
Manifest → Policy validation → Bounded execution → Receipt → Rollback
```

## 5 分钟 Demo

```bash
python -m pip install -e .
payload-lab plan examples/telemetry-demo.json
payload-lab run examples/telemetry-demo.json --receipt receipt.json
payload-lab rollback receipt.json
payload-lab build examples/telemetry-demo.json --output generated-payload.py
```

示例只包含临时标记、无害子进程、文件哈希、50ms 计算与延迟。生成文件的 SHA-256 会写入输出，便于实验复现。

## 研究价值

- **可审计载荷**：行为在 Manifest 中完整列出，生成脚本不隐藏动作。
- **遥测验证**：可观察文件、进程、计算和时间行为是否被采集。
- **安全约束**：拒绝未知动作、目录逃逸、长时间计算；无网络、持久化、凭据访问与规避模块。
- **回滚回执**：实验产生的文件记录在回执中，按工作区边界清理。

## 研究路线

下一步计划加入跨平台遥测适配器、Sigma 规则回放、实验签名、容器隔离和检测覆盖矩阵。欢迎提交新的**无害、可回滚、可观测**场景。

作者：LLR6 · MIT License
