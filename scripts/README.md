# Pipeline scripts

Run order for a sample `<name>` from `data/apks/<name>.apk` (or `.xapk`):

1. `python3 scripts/extract.py` — unzip, npci-dex string dumps, native-lib scan, summary JSON (all samples)
2. `python3 scripts/jadx_full.py` — full jadx decompile of npci-bearing dexes
3. `python3 scripts/markers.py` — feature-marker matrix (`data/markers_matrix.csv`)
4. `python3 scripts/version_table.py` — CL version per sample (`data/version-table.csv`)

Helpers: `extract_one.py` (single XAPK sample with config-split lib merge),
`dumpstrings.py` (npci-scoped dex strings).

Tools: jadx 1.5.x, apkeep, unzip, openssl, python3 (stdlib only).
