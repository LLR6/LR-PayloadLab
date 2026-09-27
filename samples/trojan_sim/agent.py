#!/usr/bin/env python3
"""LR TrojanSim agent: a deliberately harmless C2-style research sample.

Safety properties:
- connects only to loopback (127.0.0.1 / ::1)
- fixed allow-list of non-destructive commands
- no persistence, credential access, file transfer, shell execution, injection,
  privilege escalation, lateral movement, or defense evasion
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import platform
import socket
import sys
import time
from dataclasses import dataclass

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 45454
KEY_ENV = "LR_TROJAN_SIM_KEY"
ALLOWED = {"PING", "INFO", "ECHO", "SLEEP", "EXIT"}

def _key() -> bytes:
    return os.environ.get(KEY_ENV, "lr-trojan-sim-demo-key").encode()

def _sign(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(_key(), raw, hashlib.sha256).hexdigest()

def pack(payload: dict) -> bytes:
    envelope = {"payload": payload, "sig": _sign(payload)}
    return (json.dumps(envelope, separators=(",", ":")) + "\n").encode()

def unpack(line: bytes) -> dict:
    envelope = json.loads(line.decode())
    payload = envelope["payload"]
    if not hmac.compare_digest(str(envelope.get("sig", "")), _sign(payload)):
        raise ValueError("invalid message signature")
    return payload

def is_loopback(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for item in infos:
        addr = item[4][0]
        if addr not in {"127.0.0.1", "::1"}:
            return False
    return True

def machine_info() -> dict:
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
    }

def handle(command: dict) -> tuple[dict, bool]:
    name = str(command.get("cmd", "")).upper()
    if name not in ALLOWED:
        return {"ok": False, "error": "command not allowed", "cmd": name}, False
    if name == "PING":
        return {"ok": True, "reply": "PONG"}, False
    if name == "INFO":
        return {"ok": True, "info": machine_info()}, False
    if name == "ECHO":
        text = str(command.get("text", ""))[:256]
        return {"ok": True, "echo": text}, False
    if name == "SLEEP":
        seconds = max(0.0, min(float(command.get("seconds", 0.0)), 1.0))
        time.sleep(seconds)
        return {"ok": True, "slept": seconds}, False
    if name == "EXIT":
        return {"ok": True, "reply": "BYE"}, True
    return {"ok": False, "error": "unreachable"}, False

@dataclass
class Agent:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    def run(self) -> int:
        if not is_loopback(self.host):
            raise SystemExit("TrojanSim refuses non-loopback C2 targets")
        with socket.create_connection((self.host, self.port), timeout=5) as s:
            f = s.makefile("rwb")
            beacon = {
                "type": "beacon",
                "agent": "LR-TrojanSim",
                "version": "1.0",
                "info": machine_info(),
            }
            f.write(pack(beacon))
            f.flush()
            while True:
                line = f.readline()
                if not line:
                    break
                try:
                    command = unpack(line)
                    result, should_exit = handle(command)
                except Exception as exc:
                    result, should_exit = {"ok": False, "error": str(exc)}, False
                result["type"] = "result"
                f.write(pack(result))
                f.flush()
                if should_exit:
                    break
        return 0

def main() -> int:
    host = os.environ.get("LR_TROJAN_SIM_HOST", DEFAULT_HOST)
    port = int(os.environ.get("LR_TROJAN_SIM_PORT", str(DEFAULT_PORT)))
    return Agent(host, port).run()

if __name__ == "__main__":
    raise SystemExit(main())
