#!/usr/bin/env python3
"""Marker taxonomy matrix across extracted samples (CL-scoped dex strings)."""
import os, re, json, csv, glob

BASE = "/home/workspace/Projects/npci-cl-evolution/data/extracted"

MARKERS = {
    "cl_lite_version":   r'LITE_CL_VERSION|LITE_VERSION',
    "pin_pad":           r'pinactivitycomponent',
    "cl_main":           r'commonlibrary|CommonLibrary',
    "cl_services":       r'getChallenge|registerApp|getCredential|CLRemoteService',
    "cred_types":        r'CREDTYPE|ATMPIN|NMPIN|HOTP|TOTP',
    "lite_strings":      r'LITE_|[Ll]ite[A-Z]{2,}|liteMakePayment|LiteSync|GetLite',
    "atm_123pay":        r'123[Pp]ay|123PAY|HTTM|ATMPIN',
    "credit_line":       r'[Cc]redit[Ll]ine|CREDIT_LINE|creditLine',
    "nfc_tap":           r'\bNFC\b|\bHCE\b|TapAndPay|TAP_AND_PAY|tapPay',
    "conversational":    r'[Cc]onversational|HELLO_|HelloUPI|voicePay',
    "upi_circle":        r'UPI_?CIRCLE|[Dd]elegate|DPOR|secondary',
    "reserve_pay":       r'[Rr]eserve',
    "international":     r'[Ii]nternational|FOREX|fema',
    "mandate_autopay":   r'[Mm]andate|AUTOPAY|APBS',
    "block":             r'[Bb]lock[A-Z_]|BLOCK_',
    "secure_component":  r'[Ss]ecure[Cc]omponent|SECURE_COMPONENT',
    "device_binding":    r'[Dd]evice[Bb]inding|deviceId|DEVICE_ID|fingerprint',
    "aadhaar":           r'[Aa]adhaar|AADHAAR',
    "sim_retriever":     r'[Ss]msRetriever|SIM_SERIAL|getSimSerial|SIMSUB',
    "qr":                r'BHARATQR|[Bb]haratQR|QRCode|scanAndPay',
    "compound_version":  r'\b\d{1,2}\.\d{1,2}-v\d{1,2}\.\d{1,2}\b',
    "crypto_prims":      r'\bAES\b|\bRSA\b|OAEP|SHA-?256|\bGCM\b|\bCBC\b|PBKDF',
    "cert_pinning":      r'[Cc]ertificate|X509|trustStore|TrustManager',
    "otp_autoread":      r'[Oo]tp[A-Z]|OTP_|resendOTP|autoRead',
    "biometric":         r'[Bb]iometric|FingerprintManager|BIOMETRIC',
    "version_flag":      r'versionCode|versionName|sdkVersion',
    "npci_pkg":          r'L(?:in|org|com)/npci',
    "npci_dot":          r'(?:in|org|com)\.npci',
}

def main():
    samples = sorted(d for d in os.listdir(BASE)
                     if os.path.isdir(f"{BASE}/{d}") and d != "_analysis_index.json")
    rows, evidence = [], {}
    for s in samples:
        p = f"{BASE}/{s}/npci_dex_strings.txt"
        if not os.path.exists(p):
            continue
        st = open(p, encoding="utf-8", errors="ignore").read()
        evidence[s] = {}
        row = {"sample": s}
        for m, pat in MARKERS.items():
            hits = re.findall(pat, st)
            row[m] = len(hits)
            if hits:
                uniq = sorted(set(h if isinstance(h, str) else h[0] for h in hits))
                evidence[s][m] = uniq[:10]
        rows.append(row)

    fields = ["sample"] + list(MARKERS.keys())
    with open(f"{BASE}/../markers_matrix.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    json.dump(evidence, open(f"{BASE}/../markers_evidence.json", "w"), indent=1)
    print(f"matrix: {len(rows)} samples x {len(MARKERS)} markers -> {BASE}/../markers_matrix.csv")

if __name__ == "__main__":
    main()
