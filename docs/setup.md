# Setup Runbook

[Home](../README.md) · [Architecture](architecture.md) · [Next: telemetry](telemetry.md)

## Before building

Obtain valid installation media and licenses from the vendors. Select OS and Splunk versions supported together by their current compatibility guidance. Record the exact versions you actually install; none are claimed as installed by this repository.

Keep credentials outside Git. Prepare one non-administrator domain test account, separate administrator credentials and enough disk capacity for snapshots and event storage. Size VM CPU, memory and storage against the selected products' requirements and the host's available capacity; avoid presenting a guessed minimum as a supported configuration.

Create the four VMs in the [address plan](architecture.md). Take a clean snapshot before changing identity services or testing authentication.

## 1. Establish the private network

Attach the exercise adapters to the same VirtualBox internal network, `AD-LAB`. Apply static addresses from the plan; leave the gateway empty on an internal-only adapter. Check interface names inside each guest rather than copying a Linux interface name from another machine.

Use the hypervisor console to administer guests. If additional management access is required, design that path explicitly instead of bridging the exercise to a home or office LAN.

## 2. Create the Windows domain

On `ADDC01`, configure the hostname and address, then add the AD DS role through Server Manager. Promote it as a new forest using `ad.lab.test` and the NetBIOS name `LAB`. Supply the recovery password interactively. Reboot and confirm the DNS zone and domain services are available.

Create a test user such as `labuser` without domain-administrator membership. Check the effective account-lockout policy before planning any failed-authentication activity. Use a dedicated organizational unit so test policy does not affect unrelated accounts.

See Microsoft's [AD DS deployment guidance](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-).

## 3. Join the workstation

Set `TARGET-PC` to `192.168.10.100/24` and its domain DNS to `192.168.10.7`. Check name resolution before joining `ad.lab.test`. Use an authorized join account, reboot and sign in with the dedicated lab identity.

Check the resulting state from an elevated PowerShell session:

```powershell
Get-CimInstance Win32_ComputerSystem | Select-Object Name, Domain, PartOfDomain
Get-DnsClientServerAddress -AddressFamily IPv4
w32tm /query /status
```

These are commands to run, not recorded output. Verify time synchronization on both Windows hosts before comparing authentication timestamps.

## 4. Prepare the Splunk collector

Install an appropriate Splunk Enterprise package from the vendor and follow that release's installation procedure. Complete first-start licensing and administrator setup interactively. Use the supported service account and permissions; do not assume an arbitrary Linux user can start the service.

In Splunk Web, create an `endpoint` index and configure a receiving input on TCP `9997`. Restrict guest firewall access to the planned Windows senders. Keep Web access limited to the lab. Document retention and disk limits so an ingestion exercise does not exhaust the VM.

See the [Splunk installation manual](https://help.splunk.com/en/splunk-enterprise/get-started/installation-manual/9.4).

## 5. Collect Windows events

Install a supported Universal Forwarder on both Windows hosts. Configure the destination and event channels using the [telemetry guide](telemetry.md). Review service privileges and input permissions instead of broadening them indiscriminately.

Enable the applicable advanced audit policy for successful and failed logons on the test target. Capture the effective policy with `auditpol /get /category:*`; domain policy can override local choices. Keep success auditing enabled if you intend to compare failures with a later successful logon.

Sysmon is an additional endpoint source, not the provider of Security events 4624 and 4625. Select and review a Sysmon configuration separately. Do not assume that installing Sysmon alone enables every useful event category. See [Microsoft's Sysmon documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon).

## 6. Prepare a dedicated SMB test share

On `TARGET-PC`, create a folder such as `C:\LabShare` with harmless test content. Share it as `LabShare` using Windows' sharing controls. Give `LAB\labuser` only the intended read access in both the share permissions and the folder's NTFS permissions; both permission layers apply. Retain administrator access. Do not use a personal directory or grant broad write access to make the test work.

Enable only the applicable SMB inbound firewall rules for the private lab profile and restrict the remote scope to the test client. Check a legitimate interactive connection before attempting failures. Domain policy and SMB client/server settings can affect the authentication mechanism; record the actual behavior rather than forcing weaker authentication.

## 7. Snapshot the working baseline

Complete the ingestion checks before testing authentication. Save a baseline snapshot, installed-version list, network plan, effective audit policy and forwarder configuration. Exclude passwords, private keys and unrelated user information from anything intended for publication.

Continue with the [validation gates](validation.md) and the [controlled case plan](../cases/SMB-BruteForce-Detection/README.md).
