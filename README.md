# NPCI UPI Common Library — a decade of evidence

Independent, reproducible reverse-engineering history of the **NPCI UPI
Common Library (CL)** — the mandatory, NPCI-compiled component inside every
UPI app in India (PIN pad, PIN-block crypto, UPI Lite wallet, device
attestation) — plus the **UPI signer certificates** that ship with it.

Built by [CashlessConsumer](https://cashlessconsumer.in), an Indian consumer
collective. Human-supervised agentic work on Zo Computer.

**Start here:** [`report/REPORT.md`](report/REPORT.md) — the full technical
report (four eras, capability inventory, security architecture).

## Why this is public

UPI is ~2 billion transactions a day, and a single vendor-controlled library
signs every PIN entry in it. Nobody outside NPCI and the PSPs had published a
capability history of this component. Everything here is derived **only** from
publicly downloadable app builds and public NPCI circulars, and every claim in
the report is traceable to a file, hash, or string match in this repo — so you
can check it yourself.

## Verify it yourself

You do **not** need our APKs (we don't redistribute copyrighted app binaries).
Every sample is documented with source + sha256:

1. Pick a sample from [`data/INVENTORY.md`](data/INVENTORY.md) and download it
   from the listed public source (archive.org `apkarchive` items, APKPure).
2. Confirm the hash: `sha256sum <file>` against [`data/hashes.txt`](data/hashes.txt).
3. Check the shipped signer certificate — no decompilation needed:
   ```bash
   unzip -p gpay-latest.xapk '*.apk' | head -c1 >/dev/null  # if xapk, unzip first
   unzip -p com.google.android.apps.nbu.paisa.user.apk signer-upi.crt > /tmp/signer.crt
   openssl x509 -in /tmp/signer.crt -noout -dates -issuer -fingerprint -sha256
   ```
   Compare with the ready-extracted certs in [`data/certs/`](data/certs/README.md).
4. Re-run the string/decompile pipeline with `scripts/` (needs `jadx`,
   `apkeep`, `openssl`, `python3`) — see `scripts/README.md`.

Example one-liner that reproduces the headline finding on any GPay/PhonePe
build from the Play Store era 2023–2025:

```bash
unzip -p <apk> classes*.dex 2>/dev/null | strings | grep -oE "2\.3-v1\.8" | head -1
```

## Layout

| Path | Contents |
|---|---|
| `report/REPORT.md` | The technical report (evolution, capability inventory, security architecture) |
| `notes/2026-10-09-certificates.md` | Signer-certificate findings (incl. the expired-cert story) |
| `notes/2026-10-09-masp-rasp-survey.md` | MASF (May 2025) RASP survey across 5 apps + `data/rasp-matrix-2026.csv` |
| `notes/2026-10-09-method.md` | Exact method log |
| `data/INVENTORY.md`, `data/hashes.txt` | Sample provenance + sha256 for independent re-fetch |
| `data/certs/` | Extracted NPCI signer certificates + metadata table |
| `data/markers_matrix.csv`, `data/markers_evidence.json` | 17×28 feature-marker matrix with match evidence |
| `data/version-table.csv` | CL version × sample × era |
| `data/specimens/` | Decompiled `CLConstants` (2.0-era and 2.3-era) as evidence specimens |
| `data/specs/` | Archived primary docs: NPCI CL spec v1.7 PDF, Consolidated Circular v1.0 (Sep 2026) |
| `scripts/` | The full extraction/analysis pipeline |
| `data/apks/`, `data/extracted/` | **Not in this repo** (1.2 GB binaries + 3.5 GB artifacts) — re-create from the inventory |

## Headline findings

1. **Four eras:** WebView app-SDK (2016, `CL_VERSION=2.0`) → componentized Java
   library (2020) → UPI Lite wallet inside the CL (2022) → a ~3-year freeze at
   `2.3-v1.8` (2023–25) → native `libSecureComponent.so` (2025–26) → NPCI's
   server-side CL for conversational payments (Sep 2026 circular).
2. **UPI Lite's offline wallet literally lives in the CL** (SQLite store,
   key-rotation error constants) — the "offline balance" is an on-device
   database the CL guards.
3. **Every NPCI signer cert ever shipped has expired while still in
   circulating builds** — 2016 cert (expired Mar 2018) shipped into 2020;
   2022 cert (expired Jan 2024) shipped into Sep 2025; the current cert
   (expired Sep 2025) ships today. Android doesn't check signer-cert expiry
   on install/upgrade, so nothing breaks — but nobody is enforcing the
   control either.
4. **Fraud triage is not in the CL.** Screen-share/remote-access detection is
   a per-PSP implementation (Promon SHIELD RASP in GPay/PhonePe), mandated
   directionally by NPCI's MASF (May 2025) — different vendors, different
   lists, different thresholds.

## Credit

- Public discussion of the expired-certificate finding: Nemo
  ([@captn3m0](https://x.com/captn3m0), 2026-10-23). Our corpus analysis
  (2026-10-09) predates but was unpublished; his thread prompted this release.
- CL internals documentation that helped orientation early on:
  [nk521's CL gist](https://gist.github.com/nk521/c476c7fef884fed3226e6bc809a80e8c),
  [librefin-in/cl-specification](https://github.com/librefin-in/cl-specification).
- ELI5 pages: [The invisible library inside every UPI app](https://cashlessconsumer.zo.space/npci-cl-evolution)
  · [GPay's expired UPI certificate, ELI5](https://cashlessconsumer.zo.space/npci-expired-cert)- Cyber gateway: [cyber.cashlessconsumer.in/pages/npci-cl.html](https://cyber.cashlessconsumer.in/pages/npci-cl.html)

## License

Code in `scripts/`: MIT. Report, notes, and data: CC-BY-4.0. App binaries are
not included and remain the property of their publishers; extracted
certificates and constant names are factual data. NPCI, Google, PhonePe and
IDRBT are the respective owners of their trademarks and binaries; this is
independent interoperability and security research.
