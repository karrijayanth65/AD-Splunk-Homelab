# Evidence Capture Requirements

[Case](../README.md) · [Investigation plan](../reports/investigation-plan.md)

No local-run execution artifacts are included. Authorized source-lab screenshots appear in the [case overview](../README.md), with attribution and preserved values. This directory describes what to collect during your own authorized run; source captures are not proof that this guide was executed locally.

## Capture set

| Artifact | Required context | What it establishes |
|---|---|---|
| Effective audit and lockout settings | Host, command, timestamp, timezone | The test's collection and safety conditions |
| Client operation and output | Exact approved target and start/end time; no password | What the client attempted |
| Raw Security event export | Provider, event ID, record ID, host and UTC creation time | The receiving host's recorded authentication outcome |
| Splunk event and query export | Query text, time picker, timezone, index and raw-event comparison | Search behavior on the captured records |
| SMB protocol context | Same client/target/time and destination service | Why the network authentication is attributed to SMB |
| Final analyst note | Evidence references, alternatives, classification and confidence | The supported conclusion and limitations |

## Images and exports

Keep an untouched private original before redaction. Publish only reviewed screenshots and sanitized exports. A screenshot should show enough application context to interpret it; add a caption that states the host, event or query, capture context and what the image does **not** prove.

Use descriptive names such as `target-security-4625.png` or `splunk-auth-sequence.png` only after those files actually exist. Do not create a decorative image under an evidence filename. Add a full-resolution link next to each real image when it is included in the report.

## Evidence index

For each actual file, record a relative path, SHA-256, capture time with timezone, source host/tool and description. Hash the published bytes after any documented redaction; separately retain the private original hash. A hash proves byte identity, not that the activity or authorship claim is genuine.

An example PowerShell command to run against your own captured artifact is:

```powershell
Get-FileHash -LiteralPath '.\target-security-4625.png' -Algorithm SHA256
```

No hashes or execution dates are prepopulated because no such capture was supplied.
