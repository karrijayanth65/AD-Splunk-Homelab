# Troubleshooting

[Home](../README.md) · [Telemetry](telemetry.md) · [Validation](validation.md)

| Symptom | Check first | Avoid |
|---|---|---|
| Workstation cannot join the domain | Domain DNS address, DNS records, time and AD service state | Changing every DNS client to a public resolver |
| Receiver port is unreachable | Effective output target, receiver input, VM network and scoped firewall rules | Disabling all guest firewalls |
| Port works but no events appear | Index name, permissions, forwarder logs and actual Windows channel activity | Treating a TCP handshake as an ingestion test |
| Security events missing | Effective audit policy, channel access and event time range | Assuming Sysmon generates 4624/4625 |
| Sysmon source missing | Installation, reviewed configuration, channel name and service state | Importing a large unknown XML policy without review |
| Search returns no candidates | Raw events, extraction, time picker and threshold | Repeatedly generating bad passwords until an account locks |
| Many failures with no clear client | Inspect missing/loopback/translated addresses and authentication package | Assigning unrelated unknown IP values to one attacker |
| Failures followed by success | Same host/client/account, timing and approved test context | Declaring compromise without supporting activity |

## Reproduce the narrow failure

Check one stage at a time: local event, forwarder input, network path, receiver, index, extraction and detection. Keep the original error or raw record alongside the change that resolved it. If a restart is required, record it rather than attributing recovery to an unrelated edit.

Before sharing diagnostic output, remove credentials, tokens and unrelated identities. Private lab addresses in the design are examples; they do not certify the privacy of every real log field.
