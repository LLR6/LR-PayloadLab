#!/usr/bin/env python3
"""Loopback-only controller for LR TrojanSim."""
from __future__ import annotations
import json
import os
import socket
from agent import pack, unpack, DEFAULT_PORT

HELP = """Commands:
  ping
  info
  echo <text>
  sleep <0..1>
  exit
"""

def parse(text: str) -> dict | None:
    text = text.strip()
    if not text:
        return None
    head, *rest = text.split(maxsplit=1)
    cmd = head.upper()
    if cmd == "PING":
        return {"cmd": "PING"}
    if cmd == "INFO":
        return {"cmd": "INFO"}
    if cmd == "ECHO":
        return {"cmd": "ECHO", "text": rest[0] if rest else ""}
    if cmd == "SLEEP":
        try:
            seconds = float(rest[0]) if rest else 0.0
        except ValueError:
            seconds = 0.0
        return {"cmd": "SLEEP", "seconds": seconds}
    if cmd == "EXIT":
        return {"cmd": "EXIT"}
    return {"cmd": cmd}

def main() -> int:
    port = int(os.environ.get("LR_TROJAN_SIM_PORT", str(DEFAULT_PORT)))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", port))
        srv.listen(1)
        print(f"[+] TrojanSim controller listening on 127.0.0.1:{port}")
        conn, addr = srv.accept()
        with conn:
            f = conn.makefile("rwb")
            beacon = unpack(f.readline())
            print("[+] beacon:")
            print(json.dumps(beacon, ensure_ascii=False, indent=2))
            print(HELP)
            while True:
                raw = input("trojansim> ")
                if raw.strip().lower() in {"help", "?"}:
                    print(HELP)
                    continue
                command = parse(raw)
                if command is None:
                    continue
                f.write(pack(command))
                f.flush()
                response = unpack(f.readline())
                print(json.dumps(response, ensure_ascii=False, indent=2))
                if command.get("cmd") == "EXIT":
                    break
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
