# IcedID（S0483）行为研究 Case Study

## 为什么选 IcedID

IcedID 是 MITRE ATT&CK 收录的真实 Windows 恶意软件家族（S0483）。本项目不保存或分发 IcedID 恶意二进制，而是把公开威胁情报里的行为映射成可复现的检测研究对象。

研究链：

```text
IcedID public threat intelligence
        ↓
MITRE ATT&CK technique mapping
        ↓
Atomic Red Team / safe emulation coverage
        ↓
endpoint telemetry
        ↓
detection rules
        ↓
robustness / false-negative analysis
```

## 重点行为

当前 case study 选择 12 个适合做检测研究的行为：

| ATT&CK | 行为 | 研究重点 |
|---|---|---|
| T1071.001 | Web Protocols | HTTPS C2 的网络遥测 |
| T1547.001 | Registry Run Keys / Startup Folder | 启动持久化检测 |
| T1055.004 | APC Injection | 注入行为的事件关联 |
| T1055.012 | Process Hollowing | 父子进程与内存遥测 |
| T1082 | System Information Discovery | 主机信息发现 |
| T1016 | System Network Configuration Discovery | 网络配置发现 |
| T1518.001 | Security Software Discovery | 安全软件枚举 |
| T1218.007 | Msiexec | 系统二进制代理执行 |
| T1218.011 | Rundll32 | DLL 代理执行 |
| T1053.005 | Scheduled Task | 任务计划持久化 |
| T1497 | Virtualization/Sandbox Evasion | 沙箱/分析环境识别 |
| T1047 | WMI | WMI 执行行为 |

## 和 Atomic Red Team 怎么结合

Atomic Red Team 的测试按 ATT&CK technique 组织，每个 technique 都有结构化 YAML/Markdown 定义，并可由 Invoke-AtomicRedTeam 执行。

这里的研究原则是：

1. 先从 IcedID 的 ATT&CK technique 列表出发。
2. 找到相同 technique 的 Atomic Test。
3. 阅读 prerequisite / attack / cleanup 定义。
4. 只在授权、隔离测试机运行。
5. 保存 EDR/Sysmon/Windows Event Log 遥测。
6. 把测试结果喂给 LR-PayloadLab 的 detection-resilience 分析。

## 导师演示

```text
IcedID (S0483)
   │
   ├── T1082 System Information Discovery
   ├── T1016 Network Configuration Discovery
   ├── T1218.011 Rundll32
   ├── T1053.005 Scheduled Task
   └── ...
          ↓
Atomic Red Team equivalent
          ↓
Windows telemetry
          ↓
Detection / missed detection
          ↓
Feature sensitivity + detector hardening
```

重点不是声称“仓库里放了 IcedID 木马”，而是说明：

> 我选取真实恶意软件家族 IcedID 作为威胁模型，根据 ATT&CK 的公开行为证据建立可复现实验，并研究不同检测器对这些行为的覆盖和鲁棒性。

## 数据文件

- `research/icedid_case_study.json`：研究行为清单
- `research/icedid_coverage.py`：按研究战术聚合行为
- `research/evasion_benchmark.py`：检测鲁棒性实验

## 安全边界

仓库不收录真实 IcedID 二进制、不实现凭据窃取/C2/持久化/注入载荷，也不实现 AV/EDR 绕过；实验聚焦公开行为证据、授权对手模拟、遥测与检测工程。
