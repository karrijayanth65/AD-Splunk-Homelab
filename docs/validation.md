# Validation Guide

[Home](../README.md) · [Telemetry](telemetry.md) · [Case](../cases/SMB-BruteForce-Detection/README.md)

## Separate the checks

| Layer | How to verify | Claim supported |
|---|---|---|
| Repository | Local links, SVG XML and example-config structure | Files are coherent and navigable |
| Rendered presentation | Inspect GitHub pages and diagrams | Published content displays as intended |
| Ingestion | Match raw Windows records with indexed records | The actual forwarding path works |
| Detection | Execute the exact query against captured events | The search behaves on that capture |
| Investigation | Correlate artifacts and review alternatives | A bounded verdict with stated confidence |

Repository checks do not substitute for any later layer.

## Offline repository check

Python 3 is sufficient; no additional package is needed:

```bash
python scripts/check_repository.py
```

The checker validates Markdown file links, exact path casing, simple heading anchors, SVG syntax and the shape of the example forwarder stanzas. It does not execute SPL, install a forwarder, contact a Windows host or attest to any person's lab work.

Optional tools: Lychee for local/external link checking and markdownlint-cli2 for Markdown style. Online URLs can be blocked or change independently of this repository; review failures rather than hiding them with broad exclusions.

## Live-lab acceptance gates

1. Confirm isolation, addressing, DNS, time and the dedicated account's effective policies.
2. Confirm recent events from both Windows log sources reach `endpoint`.
3. Match a real raw event by host, provider, event ID, record ID and time.
4. Check the included parser on that actual XML and report missing fields.
5. Run the approved, bounded authentication test and collect the case artifacts.
6. Compare query results with the actual sequence. Record misses and false positives.
7. Write a verdict tied to evidence; review and sanitize any files before publishing.

These gates are requirements for a future execution record, not a report that they passed.
