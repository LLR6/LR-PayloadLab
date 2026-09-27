# LR-TrojanSim

一个用于课程/导师演示的 **benign trojan simulator**。它保留木马常见的 C2 架构元素——beacon、控制端、命令分发、结果回传、消息签名——但把危险能力全部裁掉。

## 能展示什么

- Agent 主动向控制端发送 beacon
- 控制端接收主机基本信息
- HMAC-SHA256 对消息做完整性校验
- 控制端下发固定 allow-list 命令
- Agent 返回执行结果
- 能抓包观察协议，也能接到检测规则/日志平台

## 安全限制

Agent **硬编码拒绝非回环地址**，因此只能连接本机 `127.0.0.1/::1`。

允许命令只有：

- `PING`
- `INFO`
- `ECHO`
- `SLEEP`（最多 1 秒）
- `EXIT`

明确不包含：

- shell / PowerShell / cmd 任意执行
- 文件上传下载
- 持久化
- 凭据读取
- 浏览器/钱包/文档窃取
- 进程注入
- 提权
- 横向移动
- 关闭或绕过 AV/EDR
- 混淆、加壳或免杀实现

## 运行

终端 A：

```bash
cd samples/trojan_sim
python server.py
```

终端 B：

```bash
cd samples/trojan_sim
python agent.py
```

控制端示例：

```text
trojansim> ping
{"ok": true, "reply": "PONG"}

trojansim> info
{"ok": true, "info": {...}}

trojansim> echo hello
{"ok": true, "echo": "hello"}

trojansim> exit
{"ok": true, "reply": "BYE"}
```

## 导师展示怎么讲

可以把它拆成 5 个模块讲：

```text
Agent startup
    ↓
Beacon
    ↓
Signed C2 protocol
    ↓
Command allow-list
    ↓
Result / audit trail
```

然后再接仓库里的 detection-evasion benchmark，展示“检测器看到这些遥测后如何分类、特征变化后为什么会漏报、如何加固”。

这份样本是为了展示木马架构和检测研究，不是可用于真实入侵的木马。
