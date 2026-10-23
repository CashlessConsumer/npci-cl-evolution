#!/usr/bin/env python3
"""Build the CL version-timeline CSV from per-sample evidence."""
import csv, json, os

BASE = "/home/workspace/Projects/npci-cl-evolution/data"
EX = f"{BASE}/extracted"

DATES = {
    "bhim-1.0": "2017 (approx; archive.org item 'BHIM 1.0'; BHIM launched 2016-12-30)",
    "bhim-2.3.1": "2020-07 (lib timestamps 2020-07-31)",
    "gpay-210.1.2": "2023-01-11 (archive.org upload)",
    "gpay-213.1.8": "2023-05-01 (archive.org upload)",
    "gpay-216.1.1": "2023-09-09 (archive.org upload)",
    "gpay-220.1.2": "2024-02-17 (archive.org upload)",
    "gpay-225.1.3": "2025-01-03 (archive.org upload)",
    "gpay-latest": "2026-10 (APKPure current)",
    "phonepe-23.12.22.0": "2023-12-22 (archive.org upload)",
    "phonepe-24.01.19.0": "2024-01-19 (archive.org upload)",
    "phonepe-24.04.19.0": "2024-04-19 (archive.org upload)",
    "phonepe-24.07.26.0": "2024-07-26 (archive.org upload)",
    "phonepe-24.11.29.0": "2024-11-29 (archive.org upload)",
    "com.phonepe.app@25.05.16.0": "2025-05-16 (APKPure)",
    "com.phonepe.app@25.09.19.0": "2025-09-19 (APKPure)",
    "com.phonepe.app@26.01.02.0": "2026-01-02 (APKPure)",
    "com.phonepe.app@26.09.11.0": "2026-09-11 (APKPure)",
}

rows = []
for s in sorted(DATES):
    d = f"{EX}/{s}"
    idx = {}
    ipath = f"{EX}/_analysis_index.json"
    if os.path.exists(ipath):
        idx = json.load(open(ipath)).get(s, {})
    cl_ver = lite_ver = ""
    cc = f"{d}/jadx-full/sources/org/npci/upi/security/pinactivitycomponent/CLConstants.java"
    for cand in (f"/tmp/cc210/sources/org/npci/upi/security/pinactivitycomponent/CLConstants.java",
                 f"/tmp/cc225/sources/org/npci/upi/security/pinactivitycomponent/CLConstants.java"):
        pass
    # CL_VERSION from strings dumps (compound pattern) or jadx source
    import glob, re, subprocess
    ver_pat = re.compile(r"\b(\d{1,2}\.\d{1,2}-v\d{1,2}\.\d{1,2})\b")
    seen = {}
    for dx in glob.glob(f"{d}/raw/app/classes*.dex") + glob.glob(f"{d}/raw/app/base/classes*.dex"):
        out = subprocess.run(f"strings -a '{dx}'", shell=True, capture_output=True, text=True).stdout
        for m in ver_pat.findall(out):
            seen[m] = seen.get(m, 0) + 1
    strs = f"{d}/npci_dex_strings.txt"
    if os.path.exists(strs):
        for m in ver_pat.findall(open(strs, errors="ignore").read()):
            seen[m] = seen.get(m, 0) + 1
    cl_ver = max(seen, key=seen.get) if seen else ""
    if s == "bhim-1.0":
        cl_ver = "2.0 (CLConstants)"
    nclasses = len(idx.get("npci_classes", []))
    libs = idx.get("cl_candidate_libs", [])
    sec = "yes" if any("SecureComponent" in l for l in libs) else ""
    rows.append({
        "sample": s, "date": DATES[s], "cl_version_observable": cl_ver,
        "npci_java_classes": nclasses, "libSecureComponent.so": sec,
        "npcl_libs": ", ".join(libs),
    })

out = f"{BASE}/version_timeline.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("wrote", out)
for r in rows:
    print(r["sample"], "|", r["cl_version_observable"], "| classes:", r["npci_java_classes"], "| native:", r["libSecureComponent.so"])
