# IcedID × Atomic Red Team Coverage Matrix

这个模块把真实威胁模型、Atomic Red Team 元数据和实验结果统一成一张 Coverage Matrix。

## 当前映射

- IcedID 研究 TTP：12
- 可找到同 ID Atomic YAML：11
- 无 exact parent-level Atomic：1（T1497）
- 高风险/容易被误用的 Atomic 只记录 metadata，不在 LR-PayloadLab 中封装执行命令。

## 生成矩阵

先复制 examples/icedid-lab-results.template.json 并填写真实实验结果。

然后运行：

    python research/atomic_coverage_matrix.py --results icedid-lab-results.json --markdown icedid-coverage.md --json icedid-coverage.json

## 实验结果字段

- run_status: not_run / passed / failed / skipped
- detection: not_evaluated / detected / missed / partial
- telemetry: 实际拿到的日志源，例如 Sysmon EID 1、Windows Security、EDR alert
- evidence: 截图、日志文件、事件编号或报告路径
- notes: 失败原因、前置条件、清理情况等

## 为什么不直接执行所有 Atomic

Process Injection、Process Hollowing、Msiexec/Rundll32 等测试可能产生高风险行为。这个仓库负责研究映射、证据记录和检测覆盖分析，不会再封装一层一键执行器。

对于 discovery、WMI、Run Key、Scheduled Task 等项目，也应只在有授权的隔离 Windows 测试主机上，阅读 upstream prerequisite / cleanup 后运行。

导师展示链路：

    IcedID TTP
       ↓
    Exact Atomic metadata
       ↓
    Authorized isolated execution
       ↓
    Telemetry evidence
       ↓
    Detection result
       ↓
    Coverage Matrix
