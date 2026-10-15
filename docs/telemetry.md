# Windows Telemetry Pipeline

[Home](../README.md) · [Setup](setup.md) · [Troubleshooting](troubleshooting.md)

## Collect before detecting

Windows writes Security events locally. A Universal Forwarder reads selected channels and sends them to the Splunk receiver. Splunk must accept the stream, store it in the intended index and make the raw records searchable before a detection can be trusted.

The example files are small, independently written lab configurations:

- [inputs.conf.example](../configs/splunk/inputs.conf.example): Security, System and Sysmon channels.
- [outputs.conf.example](../configs/splunk/outputs.conf.example): proposed collector destination.

Review these against your forwarder's supported settings before deployment. Keep `.example` files in Git; place reviewed working copies under a deliberately chosen forwarder app's `local/` directory. Do not create duplicate inputs in multiple apps.

Windows-event input and XML behavior are described in [Splunk's Windows event collection guidance](https://help.splunk.com/en/splunk-cloud-platform/administer/admin-manual/10.4.2604/get-data-into-splunk-cloud-platform/get-windows-data-into-splunk-cloud-platform). That page includes Cloud deployment steps; this repository uses a local Enterprise receiver, not the Cloud onboarding workflow.

## Inspect the effective configuration

Run these from an elevated PowerShell session on a Windows forwarder:

```powershell
& 'C:\Program Files\SplunkUniversalForwarder\bin\splunk.exe' btool inputs list --debug
& 'C:\Program Files\SplunkUniversalForwarder\bin\splunk.exe' btool outputs list --debug
Test-NetConnection 192.168.10.10 -Port 9997
```

Inspect local output privately. `btool` may show sensitive configuration and must not be published unreviewed. A successful TCP test establishes reachability, not ingestion. Restart the forwarder only after checking configuration and applicable permissions.

## Confirm the raw records

Start with a broad search rather than a query that can hide missing fields:

```spl
index=endpoint earliest=-30m
| stats count min(_time) as first_event max(_time) as last_event by host source sourcetype
| convert ctime(first_event) ctime(last_event)
```

Check both Windows hosts, recent timestamps, channel identity and raw XML. Compare an event's provider, record ID and UTC creation time with Event Viewer on the relevant host. Do not use the ingest time as a substitute for event time.

## Field contract for the included searches

The [SPL searches](../detections/README.md) explicitly extract selected fields from XML-rendered Security events. They do not require a specific add-on extraction, but they do require the raw XML structure shown by the provider. Native XML text can contain encoded entities, and parser behavior can differ. Inspect your raw records and adjust the parser before trusting results.

The search's `host` is Splunk's host metadata. Confirm that it identifies the receiving Windows machine correctly. Keep a separate source IP for the remote authentication client; the two are not interchangeable.

If an add-on already supplies reliable fields, adapt the searches to those fields and document that dependency rather than creating competing extractions. Keep a raw example privately for reproducibility.
