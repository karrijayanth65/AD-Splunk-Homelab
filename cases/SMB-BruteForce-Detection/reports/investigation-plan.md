# AD-SMB-001 Investigation Plan

[Case overview](../README.md) · [Evidence checklist](../evidence/README.md) · [Searches](../../../detections/README.md)

## Executive summary

This exercise is designed to connect a small number of authorized SMB authentication attempts to Windows Security events and a Splunk search. The proposed client is `192.168.10.250`, the target is `192.168.10.100`, and the dedicated identity is `LAB\labuser`. The investigator must establish the protocol and correlate failures with any subsequent success rather than infer compromise from a threshold alone. No run result or verdict is asserted here.

## Scope and preconditions

Use only the isolated machines in the [architecture](../../../docs/architecture.md). Confirm the test account, effective lockout policy, target permissions, time synchronization and audit coverage before beginning. Have a snapshot and a recovery path. Do not lower production protections or disable account lockout to obtain a demonstration result.

Record the start and end time with timezone, OS/Splunk versions and the authorization boundary. If these are not captured, record the gap instead of assigning a convenient date.

## Detection attributes

| Attribute | Planned value or capture requirement |
|---|---|
| Data source | Windows Security event XML from the target |
| Event family | 4625 failures; 4624 successes |
| Context | Logon Type 3 plus separate SMB context |
| Client | Proposed `192.168.10.250`; verify actual source field |
| Target | Proposed `TARGET-PC` / `192.168.10.100` |
| Account | Dedicated test identity, not an administrator |
| Threshold | Example: three failures in five minutes; adjust safely |
| Event time | Capture provider timestamp and timezone context |
| Severity | Assign after reviewing scope and impact; not preset as critical |

Microsoft documents 4625 as a failed logon and Type 3 as a network logon. Its fields include the attempted identity, status information and client address. These details support correlation, not an automatic determination of intent. See [Event 4625](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625).

## Controlled procedure

1. Confirm the target offers an explicitly approved test share and that the account has only the intended access.
2. Verify that one ordinary successful authentication is visible locally and in Splunk before introducing failures.
3. If the lockout policy safely permits it, perform a small, manually bounded set of incorrect-password attempts. Stop if the account locks, unexpected systems appear or the planned limit is reached. Use fewer attempts and a lower temporary search threshold when necessary; document that choice.
4. If the account remains usable, make one authorized successful attempt using its actual password. Do not publish the password or place it on a command line.
5. Record the client command, result, target, time and matching raw Windows records. Count events rather than assuming one command produces exactly one event.

For an interactive SMB client on the isolated Kali VM, an example invocation is:

```bash
smbclient //192.168.10.100/LabShare -p 445 -U 'LAB\labuser'
```

It prompts for a password; after a successful connection, use `ls` to inspect the harmless share and `quit` to exit. Do not use password lists, broad subnet scans or automated retries for this small correlation exercise. Check the installed client's own help and record the actual tool version and negotiated behavior.

## Analysis sequence

Use the [overview search](../../../detections/authentication-overview.spl) first. Confirm each event's host, account, client and time against the raw record. Then run the [burst candidate](../../../detections/network-failure-burst.spl) and [success correlation](../../../detections/success-after-failures.spl) searches with a narrow time picker.

Review failure status and substatus, effective lockout policy and any other traffic sharing the source/account pair. Distinguish ordinary mistakes, stale credentials and authorized testing from unexplained activity. A 4624 after failures shows a successful logon; it does not prove the password was guessed or that files were accessed. A packet/flow record or other approved protocol context is needed to substantiate SMB-specific conclusions.

## Response and closure criteria

For an unexpected real alert, follow the environment's response authority rather than applying a lab checklist blindly. Potential actions such as account restriction, source blocking or host isolation are recommendations until an authorized action record exists.

Close the lab case only after attaching the actual event sequence, parser check, query results and scope statement. Record the supported classification, confidence and reason. Do not prefill containment as completed or a malicious verdict as confirmed.
