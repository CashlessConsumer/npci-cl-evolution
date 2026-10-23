
## Addendum 2026-10-23 — public discovery by captn3m0 (Nemo); we followed

Nemo found and published this; our 9 Oct notes had the same certificates but sat unpublished. His tweets:

- Tweet: https://x.com/captn3m0/status/2113563282040844699 — "@UPI_NPCI has been running on an expired cert since Sep 2025. Issued by IDRBT, which is now managing all of *.bank.in." (screenshot table: signer-erupee.crt psosigner.npci.org.in / DigiCert EV RSA CA G2 / 2023-09-01→2024-10-01 EXPIRED; signer-upi.crt upinpci / IDRBT Sub CA 2022 / 2023-09-20→2025-09-19 EXPIRED)
- Reply (payload-encryption role): https://x.com/captn3m0/status/2113588962493337845 — "UPI uses it for encrypting payloads that reach NPCI. Not every certificate is browser/TLS."
- CBDC follow-up: https://x.com/captn3m0/status/2113565346204697073 — eRupee signer same situation; who audits it?

Match with our extraction: his upinpci dates (2023-09-20→2025-09-19) equal our GPay-2026/PhonePe-2026 signer-upi.crt exactly; his erupee end-date 2024-10-01 equals our signer-erupee.crt. Dates in his table are YYYY-MM-DD renders of the same notBefore/notAfter we read via openssl x509. New fact for us: none — but his IDRBT↔*.bank.in linkage ties the finding to the current .bank.in work, and the tweet gave it reach (17.7K views, 802 bookmarks within hours).

ELI5 page updated with the confirmation card + links: cashlessconsumer.zo.space/npci-expired-cert.
