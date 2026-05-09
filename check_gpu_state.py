#!/usr/bin/env python3
"""
check_gpu_state.py
==================
Kiểm tra trạng thái GPU và kill zombie processes trước khi chạy training mới.

Cách dùng:
    python check_gpu_state.py              # chỉ kiểm tra, không kill
    python check_gpu_state.py --kill       # kill tất cả process đang dùng GPU
    python check_gpu_state.py --kill --yes # kill không hỏi xác nhận
"""

import argparse
import os
import subprocess
import sys


def run(cmd: str, capture: bool = True) -> str:
    result = subprocess.run(
        cmd, shell=True, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE,
    )
    return (result.stdout or "").strip()


def get_gpu_info() -> str:
    return run(
        "nvidia-smi --query-gpu=index,name,memory.used,memory.free,memory.total "
        "--format=csv,noheader"
    )


def get_gpu_pids() -> list[int]:
    out = run("nvidia-smi --query-compute-apps=pid --format=csv,noheader")
    pids = []
    for line in out.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return pids


def get_zombie_pythons() -> list[tuple[int, str]]:
    """Trả về list (pid, cmdline) của python/torch processes không cần thiết."""
    out = run("ps aux")
    zombies = []
    for line in out.splitlines():
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        cmd = parts[10]
        if "python" in cmd.lower() and any(
            kw in cmd for kw in ["train_eval", "nohup", "torchrun"]
        ):
            try:
                pid = int(parts[1])
                zombies.append((pid, cmd[:80]))
            except ValueError:
                pass
    return zombies


def kill_pid(pid: int):
    try:
        os.kill(pid, 9)
        print(f"  ✓ Killed PID {pid}")
    except ProcessLookupError:
        print(f"  ⚠ PID {pid} already gone")
    except PermissionError:
        print(f"  ❌ Permission denied for PID {pid}")


def main():
    parser = argparse.ArgumentParser(description="LeJEPA — GPU state checker")
    parser.add_argument("--kill", action="store_true",
                        help="Kill tất cả process đang dùng GPU.")
    parser.add_argument("--yes",  action="store_true",
                        help="Bỏ qua confirm khi kill.")
    args = parser.parse_args()

    print("=" * 60)
    print("  GPU STATE CHECK")
    print("=" * 60)

    # ── GPU memory ──────────────────────────────────────────────
    print("\n[GPU Memory]")
    info = get_gpu_info()
    if info:
        for line in info.splitlines():
            parts = [p.strip() for p in line.split(",")]
            print(f"  GPU {parts[0]}: {parts[1]}")
            print(f"    Used  : {parts[2]}")
            print(f"    Free  : {parts[3]}")
            print(f"    Total : {parts[4]}")
    else:
        print("  ⚠ Không đọc được thông tin GPU.")

    # ── GPU processes ────────────────────────────────────────────
    print("\n[GPU Compute Processes]")
    gpu_pids = get_gpu_pids()
    if gpu_pids:
        for pid in gpu_pids:
            cmdline = run(f"cat /proc/{pid}/cmdline 2>/dev/null | tr '\\0' ' '")[:80]
            print(f"  PID {pid}: {cmdline or '(unknown)'}")
    else:
        print("  ✓ Không có process nào đang dùng GPU.")

    # ── Zombie training processes ────────────────────────────────
    print("\n[Training Processes (python/torchrun)]")
    zombies = get_zombie_pythons()
    if zombies:
        for pid, cmd in zombies:
            print(f"  PID {pid}: {cmd}")
    else:
        print("  ✓ Không có zombie training process.")

    # ── Kill section ─────────────────────────────────────────────
    all_pids = list(set(gpu_pids + [p for p, _ in zombies]))

    if args.kill and all_pids:
        print(f"\n[Kill] Sẽ kill {len(all_pids)} PID(s): {all_pids}")
        if not args.yes:
            ans = input("Xác nhận kill? [y/N] ").strip().lower()
            if ans != "y":
                print("Huỷ.")
                sys.exit(0)
        for pid in all_pids:
            kill_pid(pid)
        print("\n[Sau kill — GPU Memory]")
        print(run("nvidia-smi --query-gpu=memory.used,memory.free --format=csv,noheader"))
    elif args.kill and not all_pids:
        print("\n[Kill] Không có process nào cần kill.")
    elif not args.kill and all_pids:
        print(f"\n⚠  Có {len(all_pids)} process cần dọn. Chạy lại với --kill để xoá.")

    print("\n" + "=" * 60)
    print("  DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
