#!/usr/bin/env python3
"""Re-analyze a single XAPK sample with lib merging from config splits."""
import os, subprocess, json, glob, shutil, re, sys

BASE = "/home/workspace/Projects/npci-cl-evolution/data"
EX = f"{BASE}/extracted"
SAMPLE = sys.argv[1] if len(sys.argv) > 1 else "gpay-latest"
XAPK = f"{BASE}/apks/{SAMPLE}.xapk"

def sh(cmd, timeout=900):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

d = f"{EX}/{SAMPLE}"
if not glob.glob(f"{d}/raw/app/classes*.dex"):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    os.makedirs(f"{d}/raw/bundle", exist_ok=True)
    sh(f'unzip -oq "{XAPK}" -d {d}/raw/bundle')
bases = sorted(glob.glob(f"{d}/raw/bundle/*.apk"), key=lambda p: (("/config." in p), os.path.getsize(p)), reverse=True)
cfgs = [p for p in glob.glob(f"{d}/raw/bundle/config.*.apk")]
if bases and not glob.glob(f"{d}/raw/app/classes*.dex"):
    base = bases[0]
    os.makedirs(f"{d}/raw/app", exist_ok=True)
    sh(f'unzip -oq "{base}" -d {d}/raw/app')
for c in cfgs:
    if "arm64" in c or "armeabi" in c:
        sh(f'unzip -oq "{c}" -d {d}/raw/app')

app = f"{d}/raw/app"
dexes = sorted(os.path.basename(p) for p in glob.glob(f"{app}/classes*.dex"))
npci_dexes, npci_classes = [], set()
cls_re = re.compile(r"L((?:[a-z0-9_]+\.)+)[A-Za-z0-9_$]+;")
for dx in dexes:
    txt = sh(f'strings -a "{app}/{dx}"').stdout
    hits = re.findall(r"L(?:in|org|com)\.npci\.[A-Za-z0-9_./$]+;", txt)
    if hits:
        npci_dexes.append(dx)
        npci_classes |= {h[1:-1].replace("/", ".") for h in hits}
    if dx == dexes[0] or hits:
        with open(f"{d}/npci_dex_strings.txt", "a") as f:
            for line in txt.splitlines():
                if "npci" in line.lower() or any(k in line for k in (
                        "LITE", "Lite", "123Pay", "ATMPIN", "CreditLine", "Delegate",
                        "Reserve", "TapAndPay", "Tap", "Conversational", "HELLO",
                        "Circle", "Block", "AADHAAR", "Aadhaar", "Biometric", "Fingerprint",
                        "challenge", "getChallenge", "SSCL")):
                    f.write(line + "\n")

libs = glob.glob(f"{app}/lib/*/*.so")
so_out = open(f"{d}/so_strings.txt", "w")
cl_libs = []
for so in libs:
    txt = sh(f'strings -a "{so}"').stdout
    so_out.write(f"===== {os.path.basename(so)} =====\n{txt}\n")
    if re.search(r"secure|npci|upi|pinactivity|commonlib", os.path.basename(so), re.I) or \
       "getChallenge" in txt or "pinactivitycomponent" in txt:
        cl_libs.append(os.path.basename(so))
so_out.close()

with open(f"{d}/npci_classes.txt", "w") as f:
    f.write("\n".join(sorted(npci_classes)))

for cls in ["org.npci.upi.security.pinactivitycomponent.CLConstants"]:
    target = f"{d}/jadx"
    os.makedirs(target, exist_ok=True)
    primary = npci_dexes[0] if npci_dexes else dexes[0]
    sh(f'jadx --single-class {cls} --single-class-output "{target}/{cls}.java" "{app}/{primary}"', timeout=1200)

meta = {"sample": SAMPLE, "base_apk": os.path.basename(bases[0]) if bases else "", "dex_count": len(dexes),
        "npci_dexes": npci_dexes, "npci_classes": sorted(npci_classes),
        "lib_count": len(libs), "cl_candidate_libs": cl_libs}
idx_path = f"{EX}/_analysis_index.json"
idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
idx[SAMPLE] = meta
json.dump(idx, open(idx_path, "w"), indent=1)
print(json.dumps({k: v for k, v in meta.items() if k != "npci_classes"}, indent=1))
print("classes:", len(npci_classes))
