# Extracted UPI signer certificates — provenance and verification

These are the **public-key certificates** NPCI ships inside UPI apps for
component signing. They are public key material (anyone installing the app
receives them); we publish them so you can verify our claims without
downloading the apps.

Extracted with `unzip -p <apk> signer.crt` (or `signer-upi.crt` /
`signer-erupee.crt` in 2026 builds). Inspect any of them with:

```bash
openssl x509 -in data/certs/<file>.crt -noout -subject -issuer -dates -fingerprint -sha256
```

## The three generations

| Generation | Fingerprint (sha256, first 16) | Subject → Issuer | Validity | Shipped in (sampled) |
|---|---|---|---|---|
| 2016 | `D6:8E:52:D4:87:51:A1:EC` | `CN=upinpci` → **IDRBT CA 2014** | 31 Mar 2016 → **31 Mar 2018** | BHIM 1.0, BHIM 2.3.1 (through 2020) |
| 2022 | `58:5D:14:CB:BC:C5:24:A3` | `CN=upinpci` → **IDRBT CA 2014** | 19 Jan 2022 → **19 Jan 2024** | GPay 210.1.2 (Jan 2023) → PhonePe 25.09.19.0 (Sep 2025) |
| 2023 | `FC:F9:BE:8D:80:C7:36:72` | `CN=upinpci` → **IDRBT Sub CA 2022** | 20 Sep 2023 → **19 Sep 2025** | GPay + PhonePe current builds (Oct 2026) |
| eRupee | `C7:17:81:71:B8:81:55:9D` | `CN=psosigner.npci.org.in` (NPCI, Chennai) → **DigiCert EV RSA CA G2** | 1 Sep 2023 → **1 Oct 2024** | GPay + PhonePe current builds (Oct 2026) |

## What this means

- Every UPI signer cert NPCI has ever shipped was **allowed to expire** while
  remaining in circulating app builds. The 2016 cert expired in 2018 yet
  BHIM kept shipping it into 2020; the 2022 cert expired in Jan 2024 yet
  GPay and PhonePe builds from **Sep 2025** still carried it; the 2023 cert
  expired Sep 2025 and the **current** (Oct 2026) builds still ship it.
- The eRupee signer (a regular DigiCert EV certificate, the same class of
  certificate that browsers hard-fail on when expired) expired in Oct 2024
  and still ships in Oct 2026.
- Nothing on the device pins expiry: Android verifies the signature *chain*,
  not the validity window at install/upgrade time. Expiry is a paper control
  unless a verifier enforces it.

Discovery credit: Nemo ([@captn3m0](https://x.com/captn3m0)) publicised the
expired-cert finding on X (2026-10-23); our corpus analysis predates it
(2026-10-09, unpublished) and independently corroborates + extends it.
