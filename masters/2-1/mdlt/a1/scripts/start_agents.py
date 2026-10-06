#!/usr/bin/env python3
"""Run all three Hermes Telegram gateways in one foreground process."""

from __future__ import annotations

import signal
import subprocess
import sys
import time


PROFILES = ("coordinator", "researcher", "coder")


def main() -> None:
    processes: list[subprocess.Popen[str]] = []
    try:
        for profile in PROFILES:
            log = open(f"{profile}.log", "a", buffering=1)
            process = subprocess.Popen(
                ["hermes", "-p", profile, "gateway"],
                stdout=log,
                stderr=subprocess.STDOUT,
                text=True,
            )
            processes.append(process)
            print(f"Started {profile}: PID {process.pid}, log {profile}.log")
            time.sleep(2)
            if process.poll() is not None:
                raise RuntimeError(f"{profile} exited early; inspect {profile}.log")

        print("All gateways are running. Keep this cell active; Ctrl+C stops them.")
        while all(p.poll() is None for p in processes):
            time.sleep(2)
        failed = next(PROFILES[i] for i, p in enumerate(processes) if p.poll() is not None)
        raise RuntimeError(f"{failed} stopped; inspect {failed}.log")
    except KeyboardInterrupt:
        print("Stopping gateways...")
    finally:
        for process in processes:
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
        for process in processes:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.terminate()
    return None


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

