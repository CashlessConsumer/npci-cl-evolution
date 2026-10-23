# MASF RASP Survey — 5 UPI apps, 2026-10-09

Regulator chain: NPCI2020-21PSO001 (RASP, 2020) → NPCI2024-25IS006 (SDK handling) → **MASF, NPCI/2025-26/IS/003, 19 May 2025**: 23 controls, Identify/Protect/Detect/Respond, annual CERT-In empanelled audit by 31 Dec.

Mandatory: root/jailbreak + root-cloaking detection · install-source validation (block sideload/repackage) · runtime memory/integrity · anti-debug · obfuscation · SSL pinning (≤3 keys) · proxy detection · developer-options blocking · screen obfuscation · **screen mirroring prevention** · automated tamper response + alerting.
Recommended only: harmful-app (blacklist) detection · emulator/virtual-device blocking · device blacklisting · VPN detection · unsecured-Wi-Fi alerts · keylogger prevention · screen-overlay prevention · app lock.

Corpus (all current builds, APKPure): GPay (gpay-latest), PhonePe 26.09, Airtel Thanks 2026, WhatsApp 2026, + BHIM 2.3.1 (2020, pre-MASF baseline).
Method: strings over all classes*.dex + arm64/armeabi .so; 12-category regex (root/hook/emulator/debug/installsrc/screen/access/overlay/vpn/integrity/clone/rasp_sdk). Matrix: data/rasp-matrix-2026.csv.

Findings:
1. **Promon SHIELD RASP in GPay AND PhonePe** ("promon" fingerprints; PhonePe 59 hits). Commercial RASP is the norm at top PSPs.
2. Airtel Thanks: self-rolled RASP — root (su/magisk/supersu), hooks (frida/substrate/xposed), plus an app-CLONER watchlist in code: com.lbe.parallel, dualspace, parallel_space, shelter (installed-app blacklist check for cloners).
3. WhatsApp: root/hook detection present; screen markers (371) are its call screen-share FEATURE, not fraud RASP.
4. VPN markers: 0 in every app's strings — client-side VPN blocking is not string-evident anywhere; if done, it's server-side or via obfuscated API use.
5. Overlay/FLAG_WINDOW_IS_OBSCURED: 0 raw hits (constant may be inlined numerically — caveat).
6. BHIM 2.3.1 (2020): near-zero RASP markers — pre-MASF baseline shows the gap the 2020-21→2025 circulars closed.
7. GPay/PhonePe manifests: NO QUERY_ALL_PACKAGES; targeted <queries> only (messengers, root tools). No TeamViewer/AnyDesk entries. Screen-share blocking = RASP screen-mirroring detection (MediaProjection/VirtualDisplay), not app-list scanning.

## Installed-app checks (manifest queries extraction, 2026-10-09)

Full explicit `<queries>` packages per manifest (aapt2 xmltree):
- **PhonePe 26.09 — root/patch-tool watchlist**: amphoras.hidemyroot(+adfree), formyhm.hideroot, devadvance.rootcloak(+plus), chelpus.luckypatcher(+lackypatch), dimonvideo.luckypatcher, koushikdutta.superuser/rommanager(+license), topjohnwu.magisk, stericson.busybox, ramduino.appquarantine(+pro), yellowes.su, thirdparty.superuser, noshufou.android.su(+elite) + social (facebook katana/lite/orca) + own apps + GMS. = MASF root-cloaking detection via targeted visibility.
- **WhatsApp 2026**: com.dreamplug.androidapp (CRED!), com.google.android.apps.nbu.paisa.user (GPay), facebook family, garmin, aicore, maps — UPI/social adjacency, no security watchlist.
- **GPay 2026**: whatsapp, facebook.orca, maps/chrome/wallet, felica — no watchlist.
- **Airtel 2026**: cloner watchlist (lbe.parallel/dualspace/shelter/parallel_space) exists in CODE STRINGS but NOT in queries → likely vestigial on Android 11+ (visibility makes those checks silent no-ops) or works as virtual-container detection (dataDir paths/injected classes), which needs no visibility.

Rule: without QUERY_ALL_PACKAGES (nobody has it), an installed-app check can only target a pre-declared watchlist. Observed scope: root/patch tools only (PhonePe). No remote-access app (TeamViewer/AnyDesk) appears on any list.
