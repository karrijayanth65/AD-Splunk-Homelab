# References and Design Context

[Home](../README.md)

## Project context

[Vikram2003-07/Homelab](https://github.com/Vikram2003-07/Homelab) informed the choice of a four-machine Active Directory/Splunk lab and the SMB investigation topic. This repository's prose, examples and diagrams were written independently. Source screenshots, case findings and bundled Sysmon XML were not copied or claimed as personal execution evidence.

## Technical sources

- [Oracle VirtualBox networking modes](https://www.virtualbox.org/manual/ch06.html): virtual networking behavior and isolation choices.
- [Microsoft AD DS deployment](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-): domain-controller installation workflow.
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon): endpoint event collection and configuration.
- [Microsoft Event 4625](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625): failed-logon fields and logon types.
- [Microsoft logon auditing](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/basic-audit-logon-events): logon success/failure auditing context.
- [Splunk installation manual](https://help.splunk.com/en/splunk-enterprise/get-started/installation-manual/9.4): version-specific installation steps.
- [Splunk Windows Universal Forwarder installation](https://help.splunk.com/en/data-management/forward-data/universal-forwarder-manual/9.1/install-the-universal-forwarder/install-a-windows-universal-forwarder): Windows installation options.
- [Splunk Windows event collection examples](https://help.splunk.com/en/splunk-cloud-platform/administer/admin-manual/10.4.2604/get-data-into-splunk-cloud-platform/get-windows-data-into-splunk-cloud-platform): event-channel stanzas and XML rendering; Cloud-specific onboarding is not the local receiver design.
- [Samba smbclient manual](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html): client options and interactive credentials.

Product versions and documentation paths evolve. Use compatibility guidance for the exact versions you install. Published vendor examples explain a product; they are not evidence that a particular lab run took place.
