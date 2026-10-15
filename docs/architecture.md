# Architecture and Boundaries

[Home](../README.md) · [Setup](setup.md) · [Telemetry](telemetry.md)

## Four roles, one private segment

The design separates a domain controller, a workstation, a collector and a test client. The addresses below are a proposed lab plan, not observed host state.

| Host | Operating system | Address | Purpose |
|---|---|---|---|
| `ADDC01` | Windows Server 2022 | `192.168.10.7/24` | AD DS, DNS and domain authentication |
| `TARGET-PC` | Supported Windows Pro/Enterprise release | `192.168.10.100/24` | Domain member and authorized SMB test target |
| `SPLUNK` | Supported Ubuntu Server release | `192.168.10.10/24` | Splunk Enterprise and `endpoint` index |
| `KALI` | Kali Linux | `192.168.10.250/24` | Controlled network-authentication test client |

Domain: `ad.lab.test`. NetBIOS domain: `LAB`. Virtual network name: `AD-LAB`.

![Private lab architecture and the Windows-to-Splunk forwarding path](../assets/diagrams/lab-architecture.svg)

*Original design illustration, not a screenshot.* [Open full-size diagram](../assets/diagrams/lab-architecture.svg).

## Network choices

Use a VirtualBox internal network named `AD-LAB` for the exercise. On this internal-only segment there is no Internet gateway. Match the network name on all four adapters and assign the planned static addresses. Do not enter a gateway that does not exist.

If you need updates or installer downloads, use a temporary separate NAT adapter while the exercise is stopped. Remove or disconnect that adapter before the authentication exercise. Recheck routes and interface bindings afterward. Internal networking alone is not a substitute for guest firewalls or safe host configuration.

Windows domain members must use `192.168.10.7` for domain DNS. Set an intentional DNS-forwarding path only if Internet name resolution is needed. A temporary NAT adapter can alter routing and DNS; verify rather than assume the domain still resolves correctly.

See the [VirtualBox networking manual](https://www.virtualbox.org/manual/ch06.html) for networking modes and their boundaries.

## Data and access paths

| Path | Purpose | Limit |
|---|---|---|
| Windows forwarders → `SPLUNK:9997/TCP` | Event forwarding | Allow only planned Windows log-source addresses |
| Analyst session → Splunk Web `8000/TCP` | Search and administration | Accessible only from the isolated lab |
| `KALI` → `TARGET-PC:445/TCP` | Authorized SMB exercise | Test target only; not an Internet or office address |
| Windows member → domain DNS and AD services | Domain membership and authentication | Use AD firewall rules, not a blanket firewall disable |

The examples show a minimal internal training transport. They do not configure TLS or production access control. Use Splunk's supported encrypted-forwarding configuration before crossing an untrusted network.

## Deliberate differences from the inspiration

This design uses an internal-only exercise network, a reserved test domain, source-aware triage and explicit evidence gates. It does not reproduce the inspiration repository's screenshots, diagram or Sysmon XML file. References are kept in the [source list](REFERENCES.md).
