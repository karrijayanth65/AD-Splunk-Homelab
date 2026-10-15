# Lab Setup

[Home](README.md) · [SMB investigation](SMB-Investigation.md)

## Requirements

Use VirtualBox, valid OS installation media, Windows Server 2022 for the domain controller, a supported Windows Pro/Enterprise workstation, Ubuntu Server for Splunk and Kali Linux for the client. Check the selected Splunk release's supported OS versions and size the VMs for the host's available resources. Keep credentials outside Git.

## 1. Network

Connect all exercise adapters to the VirtualBox **internal network** `AD-LAB`, using the addresses in the [lab layout](README.md#lab-layout) and subnet mask `/24`. Leave the gateway empty on this internal-only segment. Windows domain members use `192.168.10.7` for DNS.

Use the hypervisor console for administration. A temporary separate NAT adapter can download installers while the exercise is stopped; disconnect it before testing and recheck routes and DNS. Do not bridge the exercise to a home or office network.

## 2. Active Directory

On `ADDC01`, configure the hostname and static address, install AD DS through Server Manager and promote a new forest named `ad.lab.test` with NetBIOS name `LAB`. Enter the recovery password interactively and reboot. Confirm domain DNS and services are available.

Create a non-administrator test account, `labuser`, in a dedicated lab organizational unit. Check its effective lockout policy before introducing failed logons.

Set the workstation hostname to `TARGET-PC`, configure its address and domain DNS, then join `ad.lab.test` with an authorized join account. Reboot and verify:

```powershell
Get-CimInstance Win32_ComputerSystem | Select-Object Name, Domain, PartOfDomain
Get-DnsClientServerAddress -AddressFamily IPv4
w32tm /query /status
```

Check time synchronization on both Windows hosts before comparing events.

## 3. Splunk

Install a supported Splunk Enterprise package on Ubuntu using the vendor procedure. Complete licensing and administrator setup interactively, using the supported service account. Create the `endpoint` index and a TCP `9997` receiving input.

Limit receiver access to the Windows senders. Restrict Splunk Web on TCP `8000` to the lab. Set retention and disk limits. The example transport does not configure TLS; configure supported encrypted forwarding before using an untrusted network.

## 4. Windows event forwarding

Install Universal Forwarder on both Windows machines. Review [inputs.conf.example](configs/inputs.conf.example) and [outputs.conf.example](configs/outputs.conf.example), then deploy working copies in a deliberately chosen forwarder app's `local/` directory. Avoid duplicate inputs across apps.

Enable successful and failed logon auditing on the target. Check effective policy with `auditpol /get /category:*`, since domain policy may override local settings. Install and configure Sysmon separately before enabling its input; Security events 4624 and 4625 do not come from Sysmon.

Inspect the effective configuration from an elevated PowerShell session:

```powershell
& 'C:\Program Files\SplunkUniversalForwarder\bin\splunk.exe' btool inputs list --debug
& 'C:\Program Files\SplunkUniversalForwarder\bin\splunk.exe' btool outputs list --debug
Test-NetConnection 192.168.10.10 -Port 9997
```

Review output privately for sensitive settings. A reachable port is not an ingestion test. In Splunk, start with:

```spl
index=endpoint earliest=-30m
| stats count min(_time) as first_event max(_time) as last_event by host source sourcetype
| convert ctime(first_event) ctime(last_event)
```

Confirm both Windows sources, channels and recent event times. Match a raw record's provider, event ID, record ID and UTC creation time against Event Viewer.

## 5. SMB share and baseline

On `TARGET-PC`, share a folder such as `C:\LabShare` as `LabShare`, containing harmless test files. Grant `LAB\labuser` the intended read access through both share and NTFS permissions; retain administrator access. Enable only the relevant private-profile SMB firewall rules, scoped to the test client.

Confirm ordinary access before introducing failures. Save a baseline snapshot, installed versions, network plan, audit policy and forwarding configuration. Continue with the [SMB investigation](SMB-Investigation.md).

## Troubleshooting

| Problem | Check |
|---|---|
| Domain join fails | Domain DNS, name resolution, time and AD service state |
| Receiver unreachable | VM network, output destination, input listener and scoped firewall |
| Port works but no events appear | Index, channel permissions, forwarder logs and actual channel activity |
| Security events missing | Effective audit policy and time range; Sysmon does not generate 4624/4625 |
| Search returns no results | Raw XML, field extraction, time picker and threshold |

Test one stage at a time: local event → forwarder → receiver → index → extraction → search. Do not disable firewalls or weaken lockout policy to obtain a result.

## Technical documentation

- [VirtualBox networking](https://www.virtualbox.org/manual/ch06.html)
- [Microsoft AD DS deployment](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-)
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Splunk installation](https://help.splunk.com/en/splunk-enterprise/get-started/installation-manual/9.4)
