#!/usr/bin/env python3
"""Full-dex jadx decompile of npci-bearing dexes per sample -> jadx-full/"""
import json, subprocess, os, sys, glob

BASE = "/home/workspace/Projects/npci-cl-evolution/data/extracted"
index = json.load(open(f"{BASE}/_analysis_index.json"))

for sample, meta in index.items():
    out = f"{BASE}/{sample}/jadx-full"
    done_marker = f"{out}/.done"
    if os.path.exists(done_marker):
        continue
    os.makedirs(out, exist_ok=True)
    dexes = meta.get("npci_dexes") or []
    if not dexes:
        # fall back: decompile smallest 2 dexes containing 'upi' strings
        cand = sorted(glob.glob(f"{BASE}/{sample}/raw/app/classes*.dex") if os.path.exists(f"{BASE}/{sample}/raw/app") else glob.glob(f"{BASE}/{sample}/raw/classes*.dex"), key=os.path.getsize)
        dexes = [os.path.basename(c) for c in cand[:1]]
    for d in dexes:
        paths = [p for p in (glob.glob(f"{BASE}/{sample}/raw/app/{d}") + glob.glob(f"{BASE}/{sample}/raw/{d}")) if os.path.exists(p)]
        if not paths:
            continue
        print(f"[{sample}] jadx {d} ({os.path.getsize(paths[0])//1024}KB) -> jadx-full", flush=True)
        subprocess.run(["jadx", "--no-res", "--no-debug-info", "-j", "4", "-d", out, paths[0]],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
    open(done_marker, "w").write("done")
    print(f"[{sample}] DONE", flush=True)
print("ALL DONE", flush=True)
