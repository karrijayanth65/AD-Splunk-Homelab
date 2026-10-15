# Authentication Searches

[Home](../README.md) · [Case plan](../cases/SMB-BruteForce-Detection/README.md)

| Search | Purpose | Important limitation |
|---|---|---|
| [authentication-overview.spl](authentication-overview.spl) | Inspect 4624/4625 records and extracted fields | Depends on XML-rendered raw Security events |
| [network-failure-burst.spl](network-failure-burst.spl) | Find three or more failures per host/source/account in a fixed five-minute bucket | Type 3 identifies a network logon, not SMB specifically |
| [success-after-failures.spl](success-after-failures.spl) | Find a success preceded by at least three failures in a ten-minute window | Temporal correlation is not proof of compromise |

Thresholds are deliberately small training examples. Adjust them to the test account's lockout policy and the environment's baseline; do not induce a lockout to make a query return a result. The searches have not been executed against a live Splunk instance as part of this documentation work.

## Validate the assumptions

Confirm the `endpoint` index, host attribution and raw XML tags before using these searches. The regexes read unprefixed `EventID` and named `Data` elements from typical Windows XML. Different namespaces or formatting may require a proper XML extraction or adjusted field mapping. XML-encoded account names need decoding before identity correlation.

Check for missing fields with the overview search. Bursts exclude events without a source IP or account instead of grouping unrelated unknowns together. Normalize IPv4-mapped IPv6 addresses consistently if they occur in your capture.

The five-minute search uses fixed buckets; attempts split across a bucket boundary may not reach its threshold. The success search sorts the selected event set and uses a rolling ten-minute window; large time ranges can be expensive. Set a narrow time picker, inspect the event sequence and account for identical event timestamps before reaching a conclusion.

To connect the candidate to SMB, correlate the same client and target with the approved test command, target-side context and network telemetry for TCP 445. Do not interpret a client's ephemeral source port as the SMB destination port.
