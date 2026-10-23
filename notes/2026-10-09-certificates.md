# CL ships with certificates — corpus evidence (2026-10-09)

## What ships (APK root, all GPay + PhonePe samples)

| Cert | Samples | Subject | Issuer | Validity | Key (sha1 of pubkey) |
|---|---|---|---|---|---|
| `signer.crt` | GPay 210/213/216/220/225, PhonePe 23.12/24.11/25.09 | CN=upinpci | IDRBT CA 2014 (RBI-backed banking CA, Hyderabad) | 2022-01-19 → 2024-01-19 | aad46e0cd0c0 |
| `signer-upi.crt` | GPay 2026, PhonePe 26.01/26.09 | CN=upinpci | IDRBT Sub CA 2022 (state field updated: Andhra Pradesh → Telangana) | 2023-09-20 → 2025-09-19 | aad46e0cd0c0 (SAME key) |
| `signer-erupee.crt` | GPay 2026, PhonePe 26.01/26.09 | CN=psosigner.npci.org.in, O=National Payments Corporation of India (Chennai), EV | DigiCert EV RSA CA G2 | 2023-09-01 → 2024-10-01 | 7a25dd57348f |

Non-NPCI certs present but unrelated: GPay `res/dI.der` = Google Trust Services GTS Root R1 (Flutter/GMS); `assets/android_release.assets/roots.pem` = Flutter root store. PhonePe `assets/public_key_params_{prod,stage,preprod}` = cached server key-config JSON (clientId ANDROID, namespace CARD_ENCRYPTION), not NPCI certs. BHIM 1.0 `assets/remoteAssetPublicKey` = key for verifying remotely fetched assets (Juspay-era; same filename reappears in PhonePe's `juspay/` asset dir).

## Findings

1. **Yes — the CL ships certificates.** One NPCI UPI cert at the APK root since at least Jan 2023 (GPay 210). Matches spec v1.7 §"Verify the common library authenticity" (jarsigner on the NPCI-signed AAR) and the challenge-encryption flow: the CL extracts the public key from the bundled CRT and RSA-OAEP-wraps the challenge/key pipe for NPCI to unwrap server-side.
2. **Key continuity, cert churn.** upinpci's public key (sha1 aad46e0cd0c0) is identical across the 2022 and 2023 certs — NPCI rotated certificates (new IDRBT Sub CA 2022 chain; issuer address updated for the state rename) but kept the same key pair since ≥2022.
3. **Expiry is not enforced.** Every pre-2026 build ships `signer.crt` ~8–24 months past its 2024-01-19 expiry (GPay 225 Jan 2025, PhonePe 25.09 Sep 2025). All three certs in 2026 builds are past notAfter (upi: expired 2025-09; erupee: expired 2024-10). Consistent with nk521's finding that an expired bundled CRT is still trusted because it isn't on the CRL. The cert functions as a key container; nothing in the client path validates the X.509 chain — trust is anchored in NPCI's distribution pipeline, not PKI.
4. **2026 adds per-rail certs.** `signer-upi.crt` + `signer-erupee.crt` appear together in both GPay 2026 and PhonePe 26.x — the CL/app bundle now carries NPCI credentials for UPI *and* e₨ (e-Rupee). First corpus evidence of the e₨ rail sharing the UPI app's security plumbing.
5. **The erupee cert is a different PKI lineage.** DigiCert EV (public web CA), CN=psosigner.npci.org.in — NPCI's organization-signer identity — vs the IDRBT (banking-CA) lineage for upinpci. Two trust anchors in one APK.

## Files
- gpay-210.1.2/gpay-225.1.3, phonepe-24.11.29.0, com.phonepe.app@25.09.19.0: `raw/app/signer.crt`
- gpay-latest, com.phonepe.app@26.01.02.0, com.phonepe.app@26.09.11.0: `raw/app/signer-upi.crt`, `raw/app/signer-erupee.crt`
- Verify: `openssl x509 -in <path> -noout -subject -issuer -dates`
