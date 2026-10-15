# Project Bible

## Decisions

| Item | Decision |
|---|---|
| Project | AD-Splunk-Homelab |
| Documentation maintainer | Jayanth K |
| Documentation date | 15 October 2026 |
| Scope | Original build guide, example configurations, searches and investigation plan |
| Publication | User requested a new public repository after validation |
| Source assets | No copied execution screenshots, source report or bundled Sysmon XML |
| Visuals | Two original editable SVG design illustrations |
| Execution evidence | Not supplied; no personal live-lab run is claimed |

## Technical contract

The private lab uses `192.168.10.0/24`, `AD-LAB`, the domain `ad.lab.test` and NetBIOS name `LAB`. Windows sources forward XML-rendered events to the proposed Splunk receiver at `192.168.10.10:9997`, using the `endpoint` index. Configurations are examples, not a production security baseline.

Keep the network plan, configuration examples, diagrams and search assumptions consistent. Type 3 alone does not establish SMB. A later successful logon alone does not establish compromise.

## Verification boundaries

Use [the validation guide](docs/validation.md). Record repository validation separately from live ingestion, search execution and analyst conclusions. No Windows or Splunk environment was accessed to create this documentation. Genuine execution artifacts can be added after an authorized run and privacy review.

References and inspiration are documented in [REFERENCES.md](docs/REFERENCES.md). Private workspace paths, local audit records and credentials do not belong in the public project.
