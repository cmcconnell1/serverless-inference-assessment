# Status page components and incident statistics

Source: Atlassian Statuspage summary.json and incidents.json captured by the probe
script (DeepInfra does not expose a Statuspage API; see api-surface.md).

Incident minutes are start to resolved as posted by the provider. Statuspage returns
the 50 most recent incidents, so a 90 day window may be truncated where noted.
Windows end at the capture time of incidents.json. An incident tagged on several
components with the same name (for example one per region) counts once per name.
Reference downtime budgets per 30 days: 99.99% = 4.4 min, 99.95% = 21.9 min,
99.9% = 43.8 min, 99.5% = 219 min.

## akamai: Linode (https://status.linode.com)

Components: 250 total, 8 groups, 242 leaf. Page updated 2026-09-29T18:06:06.990Z.

Groups: Regions, Backups, Block Storage, NodeBalancers, Object Storage, Linode Kubernetes Engine, Metadata Service, Observability

Leaf component names: AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (Tokyo 2) (x2), AP-Northeast-2 (Tokyo 2) Backups, AP-Northeast-2 (Tokyo 2) Block Storage, AP-Northeast-2 (Tokyo 2) NodeBalancers, AP-South (Singapore) (x2), AP-South (Singapore) Backups, AP-South (Singapore) Block Storage, AP-South (Singapore) Linode Kubernetes Engine, AP-South (Singapore) NodeBalancers, AP-South (Singapore) Object Storage, AP-Southeast (Sydney) (x2), AP-Southeast (Sydney) Backups, AP-Southeast (Sydney) Block Storage, AP-Southeast (Sydney) Linode Kubernetes Engine, AP-Southeast (Sydney) NodeBalancers, AP-West (Mumbai) (x2), AP-West (Mumbai) Backups, AP-West (Mumbai) Block Storage, AP-West (Mumbai) Linode Kubernetes Engine, AP-West (Mumbai) NodeBalancers, AU-MEL (Melbourne) (x3), AU-MEL (Melbourne) Backups, AU-MEL (Melbourne) Block Storage, AU-MEL (Melbourne) Linode Kubernetes Engine, AU-MEL (Melbourne) NodeBalancers, AU-MEL (Melbourne) Object Storage, Akamai Cloud Pulse (ACLP) - Alerts, Akamai Cloud Pulse (ACLP) - Logs, Akamai Cloud Pulse (ACLP) - Metrics, BR-GRU (Sao Paulo) Object Storage, BR-GRU (São Paulo) (x2), BR-GRU (São Paulo)  Linode Kubernetes Engine, BR-GRU (São Paulo) Backups, BR-GRU (São Paulo) Block Storage, BR-GRU (São Paulo) NodeBalancers, CA-Central (Toronto) (x2), CA-Central (Toronto) Backups, CA-Central (Toronto) Block Storage, CA-Central (Toronto) Linode Kubernetes Engine, CA-Central (Toronto) NodeBalancers, CL-SCL (Santiago) (x2), CO-BOG (Bogota) (x2), Cloud Manager and API, DE-FRA-2 (Frankfurt 2) (x2), DE-FRA-2 (Frankfurt 2) Backups, DE-FRA-2 (Frankfurt 2) Block Storage, DE-FRA-2 (Frankfurt 2) Linode Kubernetes Engine, DE-FRA-2 (Frankfurt 2) NodeBalancers, DE-FRA-2 (Frankfurt 2) Object Storage, DE-HAM (Hamburg) (x2), ES-MAD (Madrid) (x2), ES-MAD (Madrid) Backups, ES-MAD (Madrid) Block Storage, ES-MAD (Madrid) Linode Kubernetes Engine, ES-MAD (Madrid) NodeBalancers, ES-MAD (Madrid) Object Storage, EU-Central (Frankfurt) (x2), EU-Central (Frankfurt)  NodeBalancers, EU-Central (Frankfurt) Backups, EU-Central (Frankfurt) Block Storage, EU-Central (Frankfurt) Linode Kubernetes Engine, EU-Central (Frankfurt) Object Storage, EU-West (London) (x2), EU-West (London) Backups, EU-West (London) Block Storage, EU-West (London) Linode Kubernetes Engine, EU-West (London) NodeBalancers, FR-MRS (Marseille) (x2), FR-PAR (Paris) (x2), FR-PAR (Paris) Backups, FR-PAR (Paris) Block Storage, FR-PAR (Paris) Linode Kubernetes Engine, FR-PAR (Paris) NodeBalancers, FR-PAR (Paris) Object Storage, FR-PAR-2 (Paris 2), GB-LON (London 2) (x3), GB-LON (London 2) Backups, GB-LON (London 2) Block Storage, GB-LON (London 2) Linode Kubernetes Engine, GB-LON (London 2) NodeBalancers, GB-LON (London 2) Object Storage, Hosted DNS Service, ID-CGK (Jakarta) (x2), ID-CGK (Jakarta) Backups, ID-CGK (Jakarta) Block Storage, ID-CGK (Jakarta) Linode Kubernetes Engine, ID-CGK (Jakarta) NodeBalancers, ID-CGK (Jakarta) Object Storage, IN-BOM-2 (Mumbai 2) (x2), IN-BOM-2 (Mumbai 2) Backups, IN-BOM-2 (Mumbai 2) Block Storage, IN-BOM-2 (Mumbai 2) Linode Kubernetes Engine, IN-BOM-2 (Mumbai 2) NodeBalancers, IN-BOM-2 (Mumbai 2) Object Storage, IN-MAA (Chennai) (x2), IN-MAA (Chennai) Backups, IN-MAA (Chennai) Block Storage, IN-MAA (Chennai) Linode Kubernetes Engine, IN-MAA (Chennai) NodeBalancers, IN-MAA (Chennai) Object Storage, IT-MIL (Milan) (x2), IT-MIL (Milan) Backups, IT-MIL (Milan) Block Storage, IT-MIL (Milan) Linode Kubernetes Engine, IT-MIL (Milan) NodeBalancers, IT-MIL (Milan) Object Storage, JP-OSA (Osaka) (x2), JP-OSA (Osaka) Backups, JP-OSA (Osaka) Block Storage, JP-OSA (Osaka) Linode Kubernetes Engine, JP-OSA (Osaka) NodeBalancers, JP-OSA (Osaka) Object Storage, JP-TYO-3 (Tokyo 3) (x2), JP-TYO-3 (Tokyo 3) Block Storage, JP-TYO-3 (Tokyo 3) Linode Kubernetes Engine, JP-TYO-3 (Tokyo 3) NodeBalancers, JP-TYO-3 (Tokyo 3) Object Storage, JP-TYO-3 (Tokyo) Backups, Linode.com, Longview, MX-QRO (Queretaro) (x2), MY-KUL (Kuala Lumpur) (x2), Managed Databases, NL-AMS (Amsterdam) (x2), NL-AMS (Amsterdam) Backups, NL-AMS (Amsterdam) Block Storage, NL-AMS (Amsterdam) Linode Kubernetes Engine, NL-AMS (Amsterdam) NodeBalancers, NL-AMS (Amsterdam) Object Storage, NZ-AKL (Auckland) (x2), SE-STO (Stockholm) (x2), SE-STO (Stockholm) Backups, SE-STO (Stockholm) Block Storage, SE-STO (Stockholm) Linode Kubernetes Engine, SE-STO (Stockholm) NodeBalancers, SE-STO (Stockholm) Object Storage, SG-SIN-2 (Singapore 2) (x2), SG-SIN-2 (Singapore 2) Backups, SG-SIN-2 (Singapore 2) Block Storage, SG-SIN-2 (Singapore 2) Linode Kubernetes Engine, SG-SIN-2 (Singapore 2) NodeBalancers, SG-SIN-2 (Singapore 2) Object Storage, US-Central (Dallas) (x2), US-Central (Dallas) Backups, US-Central (Dallas) Block Storage, US-Central (Dallas) Linode Kubernetes Engine, US-Central (Dallas) NodeBalancers, US-DEN (Denver) (x2), US-East (Newark) (x2), US-East (Newark) Backups, US-East (Newark) Block Storage, US-East (Newark) Linode Kubernetes Engine, US-East (Newark) NodeBalancers, US-East (Newark) Object Storage, US-HOU (Houston) (x2), US-IAD (Washington) (x2), US-IAD (Washington) Backups, US-IAD (Washington) Block Storage, US-IAD (Washington) Linode Kubernetes Engine, US-IAD (Washington) NodeBalancers, US-IAD (Washington) Object Storage, US-IAD-2 (Washington 2), US-LAX (Los Angeles) (x2), US-LAX (Los Angeles) Backups, US-LAX (Los Angeles) Block Storage, US-LAX (Los Angeles) Linode Kubernetes Engine, US-LAX (Los Angeles) NodeBalancers, US-LAX (Los Angeles) Object Storage, US-MIA (Miami) (x2), US-MIA (Miami) Backups, US-MIA (Miami) Block Storage, US-MIA (Miami) Linode Kubernetes Engine, US-MIA (Miami) NodeBalancers, US-MIA (Miami) Object Storage, US-ORD (Chicago) (x2), US-ORD (Chicago) Backups, US-ORD (Chicago) Block Storage, US-ORD (Chicago) Linode Kubernetes Engine, US-ORD (Chicago) NodeBalancers, US-ORD (Chicago) Object Storage, US-SEA (Seattle) (x2), US-SEA (Seattle) Backups, US-SEA (Seattle) Block Storage, US-SEA (Seattle) Linode Kubernetes Engine, US-SEA (Seattle) NodeBalancers, US-SEA (Seattle) Object Storage, US-Southeast (Atlanta) (x2), US-Southeast (Atlanta) Backups, US-Southeast (Atlanta) Block Storage, US-Southeast (Atlanta) Linode Kubernetes Engine, US-Southeast (Atlanta) NodeBalancers, US-Southeast (Atlanta) Object Storage, US-West (Fremont) (x2), US-West (Fremont) Backups, US-West (Fremont) Block Storage, US-West (Fremont) Linode Kubernetes Engine, US-West (Fremont) NodeBalancers, ZA-JNB (Johannesburg) (x2)

Incidents returned: 50 (oldest 2026-04-24). Window end: 2026-09-29T18:23:01Z.

### Last 30 days

Incidents: 4 (minor: 3, none: 1). Resolved incident-minutes summed across incidents: 2733.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| Cloud Manager and API | 3 | 2298 | 0 | 0 | 100.000% |
| AP-Northeast-2 (Tokyo 2) | 1 | 2053 | 0 | 0 | 100.000% |
| AP-South (Singapore) | 1 | 2053 | 0 | 0 | 100.000% |
| AP-Southeast (Sydney) | 1 | 2053 | 0 | 0 | 100.000% |
| AP-West (Mumbai) | 1 | 2053 | 0 | 0 | 100.000% |
| AU-MEL (Melbourne) | 1 | 2053 | 0 | 0 | 100.000% |
| BR-GRU (São Paulo) | 1 | 2053 | 0 | 0 | 100.000% |
| CA-Central (Toronto) | 1 | 2053 | 0 | 0 | 100.000% |
| CL-SCL (Santiago) | 1 | 2053 | 0 | 0 | 100.000% |
| CO-BOG (Bogota) | 1 | 2053 | 0 | 0 | 100.000% |
| DE-FRA-2 (Frankfurt 2) | 1 | 2053 | 0 | 0 | 100.000% |
| DE-HAM (Hamburg) | 1 | 2053 | 0 | 0 | 100.000% |
| ES-MAD (Madrid) | 1 | 2053 | 0 | 0 | 100.000% |
| EU-Central (Frankfurt) | 1 | 2053 | 0 | 0 | 100.000% |
| EU-West (London) | 1 | 2053 | 0 | 0 | 100.000% |
| FR-MRS (Marseille) | 1 | 2053 | 0 | 0 | 100.000% |
| FR-PAR (Paris) | 1 | 2053 | 0 | 0 | 100.000% |
| FR-PAR-2 (Paris 2) | 1 | 2053 | 0 | 0 | 100.000% |
| GB-LON (London 2) | 1 | 2053 | 0 | 0 | 100.000% |
| ID-CGK (Jakarta) | 1 | 2053 | 0 | 0 | 100.000% |
| IN-BOM-2 (Mumbai 2) | 1 | 2053 | 0 | 0 | 100.000% |
| IN-MAA (Chennai) | 1 | 2053 | 0 | 0 | 100.000% |
| IT-MIL (Milan) | 1 | 2053 | 0 | 0 | 100.000% |
| JP-OSA (Osaka) | 1 | 2053 | 0 | 0 | 100.000% |
| JP-TYO-3 (Tokyo 3) | 1 | 2053 | 0 | 0 | 100.000% |

### Last 90 days

Incidents: 22 (minor: 9, none: 13). Resolved incident-minutes summed across incidents: 29618.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| (no component tagged) | 3 | 16011 | 0 | 0 | 100.000% |
| US-SEA (Seattle) | 5 | 10280 | 0 | 0 | 100.000% |
| US-MIA (Miami) | 4 | 9566 | 0 | 0 | 100.000% |
| IN-BOM-2 (Mumbai 2) | 3 | 9566 | 0 | 0 | 100.000% |
| IN-MAA (Chennai) | 3 | 9566 | 0 | 0 | 100.000% |
| US-Central (Dallas) | 3 | 9566 | 0 | 0 | 100.000% |
| US-DEN (Denver) | 3 | 9566 | 0 | 0 | 100.000% |
| US-East (Newark) | 3 | 9566 | 0 | 0 | 100.000% |
| US-HOU (Houston) | 3 | 9566 | 0 | 0 | 100.000% |
| US-IAD (Washington) | 3 | 9566 | 0 | 0 | 100.000% |
| US-IAD-2 (Washington 2) | 3 | 9566 | 0 | 0 | 100.000% |
| US-LAX (Los Angeles) | 3 | 9566 | 0 | 0 | 100.000% |
| US-ORD (Chicago) | 3 | 9566 | 0 | 0 | 100.000% |
| US-Southeast (Atlanta) | 3 | 9566 | 0 | 0 | 100.000% |
| US-West (Fremont) | 3 | 9566 | 0 | 0 | 100.000% |
| IT-MIL (Milan) | 4 | 3556 | 0 | 0 | 100.000% |
| AP-Northeast-2 (Tokyo 2) | 2 | 3340 | 0 | 0 | 100.000% |
| AP-South (Singapore) | 2 | 3340 | 0 | 0 | 100.000% |
| AP-Southeast (Sydney) | 2 | 3340 | 0 | 0 | 100.000% |
| AP-West (Mumbai) | 2 | 3340 | 0 | 0 | 100.000% |
| AU-MEL (Melbourne) | 2 | 3340 | 0 | 0 | 100.000% |
| BR-GRU (São Paulo) | 2 | 3340 | 0 | 0 | 100.000% |
| CA-Central (Toronto) | 2 | 3340 | 0 | 0 | 100.000% |
| CL-SCL (Santiago) | 2 | 3340 | 0 | 0 | 100.000% |
| CO-BOG (Bogota) | 2 | 3340 | 0 | 0 | 100.000% |

### Incident log (most recent 50)

| Created (UTC) | Impact | Minutes | Components | Title |
| --- | --- | --- | --- | --- |
| 2026-09-25T15:09 | minor | 72 | Cloud Manager and API | Service Issue - Cloud Manager and API |
| 2026-09-21T17:13 | minor | 2053 | AP-Northeast-2 (Tokyo 2), AP-South (Singapore), AP-Southeast (Sydne... | Emerging Service Issue - Cloud Manager and API |
| 2026-09-21T16:50 | none | 435 | Hosted DNS Service | Emerging Service Issue - [DNS] - [eu-west] |
| 2026-09-07T10:38 | minor | 173 | Cloud Manager and API | Service Issue - Cloud Manager and API |
| 2026-08-28T10:26 | none | 438 | Linode.com, US-SEA (Seattle) | Service Issue - US-SEA (Seattle, WA) |
| 2026-08-24T21:52 | none | 198 | US-SEA (Seattle) Object Storage | Service Issue - Object Storage - US-SEA |
| 2026-08-21T17:23 | none | 276 | US-SEA (Seattle) | Service Issue - US-SEA (Seattle, WA) |
| 2026-08-10T17:15 | none | 15926 |  | Upstream Issues - Ubuntu |
| 2026-08-14T20:13 | minor | 77 | IT-MIL (Milan) | Connectivity Issue - IT-MIL (Milan) data center |
| 2026-08-13T18:46 | none | 340 | Cloud Manager and API | Emerging Service Issue - API - All Regions |
| 2026-08-13T21:13 | minor | 132 | US-IAD (Washington) Linode Kubernetes Engine | Service Issue - Linode Kubernetes Engine Enterprise (LKE-E)- IAD2 (Washington) |
| 2026-08-13T16:16 | minor | 98 | US-IAD (Washington) Linode Kubernetes Engine | Service Issue - Linode Kubernetes Engine (IAD2) |
| 2026-08-13T14:00 | none | -1547 |  | Service Issue - Linode Kubernetes Engine Enterprise (LKE-E) - Seattle (SEA1) |
| 2026-07-31T17:49 | none | 6225 | IN-BOM-2 (Mumbai 2), IN-MAA (Chennai), US-Central (Dallas), US-DEN ... | Upstream Loss - Some Paths (in-maa/in-bom-2 to US Region) |
| 2026-07-28T18:14 | none | 1093 | AP-Northeast-2 (Tokyo 2) Block Storage, AP-South (Singapore) Block ... | Service Issue - Host Job Performance Degradation - Several Regions |
| 2026-07-20T01:52 | minor | 139 | IT-MIL (Milan) | Connectivity Issue - Linodes in Milan, Italy |
| 2026-07-18T03:34 | minor | 62 | FR-PAR (Paris) Object Storage, US-IAD (Washington) Object Storage, ... | Service Issue - Object Storage |
| 2026-07-16T01:24 | none | 0 | US-MIA (Miami) | Connectivity Issue - US-MIA (Miami |
| 2026-07-14T12:21 | minor | 425 | Cloud Manager and API | Service Issue - Linode API/CLI |
| 2026-07-13T18:29 | none | 85 |  | Service Issue - Host Jobs - All Regions |
| 2026-07-09T16:57 | none | 83 | Cloud Manager and API | Emerging Service Issue - Cloud Manager |
| 2026-06-26T17:35 | minor | 16971 | Akamai Cloud Pulse (ACLP) - Metrics | Service Issue - ACLP Metrics |
| 2026-07-06T18:04 | none | 1287 | AP-Northeast-2 (Tokyo 2), AP-South (Singapore), AP-Southeast (Sydne... | Emerging Service Issue - Managed Databases - All Regions |
| 2026-05-13T21:02 | minor | 77380 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (To... | [Fragnesia] Linux Privilege Escalation Vulnerability |
| 2026-05-08T13:40 | minor | 85021 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (To... | [DirtyFrag] Linux Privilege Escalation Vulnerability |
| 2026-07-01T17:21 | none | 66 | Cloud Manager and API | Service Issue - Linode Automated Networking |
| 2026-06-30T18:54 | minor | 268 | SG-SIN-2 (Singapore 2) Block Storage | Service Issue - Block Storage - Singapore Expansion, SP (sg-sin-2) |
| 2026-06-26T17:14 | none | 139 | US-IAD (Washington) | Connectivity Issue - US-IAD |
| 2026-06-24T18:53 | none | 1476 | AP-Northeast-2 (Tokyo 2), AP-South (Singapore), AP-Southeast (Sydne... | Emerging Service Issue - GPU Instances - All Regions |
| 2026-06-25T14:33 | none | 248 | AP-Northeast-2 (Tokyo 2), AP-South (Singapore), AP-Southeast (Sydne... | Emerging Service Issue - Migrations |
| 2026-06-24T16:27 | none | 0 |  | Service Issue - Debian Package Availability |
| 2026-06-16T14:29 | none | 169 | US-MIA (Miami) | Emerging Service Issue - Networking - US-MIA (Miami) |
| 2026-06-16T08:56 | minor | 258 | Longview | Service Issue: Longview |
| 2026-06-16T03:44 | none | 142 |  | Emerging Service Issue - Linode Migrations |
| 2026-06-02T01:26 | maintenance | 9729 | Linode.com | Linode Community Maintenance |
| 2026-06-05T14:23 | none | 35 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-South (Singapor... | Emerging Service Issue - LKE Enterprise - All Regions |
| 2026-06-03T14:22 | none | 1529 |  | Emerging Service Issue - Support Phone Line |
| 2026-06-03T08:58 | minor | 1454 | US-East (Newark) Block Storage | Service Issue - Block Storage Newark, US |
| 2026-05-29T18:23 | none | 0 | GB-LON (London 2) Object Storage | Service Issue - Object Storage |
| 2026-05-22T11:22 | minor | 5453 | FR-PAR (Paris) | Service Issue - Paris (FR-PAR3) |
| 2026-05-19T19:48 | none | 279 |  | Emerging Service Issue - GPU Deployment |
| 2026-05-16T00:42 | none | 61 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (To... | Service Issue - [Linodes and Linode Kubernetes Engine (LKE)] - [All Regions] |
| 2026-05-15T02:24 | none | 88 |  | Investigating - Linode VM Migration Delays (All Regions) |
| 2026-05-13T09:42 | minor | 295 | NL-AMS (Amsterdam) | Connectivity Issue - NL-AMS |
| 2026-05-12T17:12 | minor | 470 | AP-West (Mumbai), IN-MAA (Chennai) | Connectivity Issue - AP-West (Mumbai) and IN-MAA (Chennai) |
| 2026-05-12T21:00 | none | 0 |  | Service Issue - ACLP Logs |
| 2026-05-01T17:51 | minor | 6028 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (To... | (Copy Fail) Linux Kernel Local Privilege Escalation Vulnerability [CVE-2026-31431] |
| 2026-04-28T17:17 | minor | 7825 | IN-MAA (Chennai) | Service Issue - Connectivity Issues - Chennai (IN-MAA) |
| 2026-04-29T09:22 | minor | 598 | AP-South (Singapore) Object Storage, AU-MEL (Melbourne), AU-MEL (Me... | Object Storage Key creation and validation failing with error 403 in multiple data centers |
| 2026-04-24T19:27 | minor | 5509 | AP-Northeast (Tokyo 2) Linode Kubernetes Engine, AP-Northeast-2 (To... | Service Issue - Linode Kubernetes Engine (LKE) |

## baseten: Baseten (https://status.baseten.co)

Components: 6 total, 0 groups, 6 leaf. Page updated 2026-09-29T11:06:11.723-07:00.

Leaf component names: Dedicated Inference, Homepage and Docs, Model APIs, Model Management API, Training, Web Application

Incidents returned: 50 (oldest 2026-05-26). Window end: 2026-09-29T18:21:45Z.

### Last 30 days

Incidents: 11 (major: 5, minor: 6). Resolved incident-minutes summed across incidents: 349.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| Dedicated Inference | 6 | 214 | 4 | 86 | 99.800% |
| Model APIs | 3 | 103 | 1 | 55 | 99.873% |
| Model Management API | 2 | 32 | 0 | 0 | 100.000% |
| Web Application | 1 | 21 | 0 | 0 | 100.000% |

### Last 90 days

Incidents: 35 (major: 8, minor: 27). Resolved incident-minutes summed across incidents: 1385.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| Model APIs | 12 | 608 | 4 | 299 | 99.769% |
| Dedicated Inference | 17 | 453 | 4 | 86 | 99.933% |
| Model Management API | 6 | 324 | 0 | 0 | 100.000% |
| Web Application | 3 | 124 | 0 | 0 | 100.000% |

### Incident log (most recent 50)

| Created (UTC) | Impact | Minutes | Components | Title |
| --- | --- | --- | --- | --- |
| 2026-09-29T01:12 | major | 13 | Dedicated Inference | Elevated 500s in Single us-central Region |
| 2026-09-28T18:07 | minor | 21 | Model Management API, Web Application | Metrics degradation in UI and API. **Inference not affected** |
| 2026-09-24T11:35 | minor | 82 | Dedicated Inference | Intermittent 5xx for a subset of models in 1 US Central cluster |
| 2026-09-24T00:23 | major | 42 | Dedicated Inference | Elevated inference 500s for a subset of models deployed in 1 US-East cluster |
| 2026-09-21T11:34 | major | 7 | Dedicated Inference | Elevated inference 500s for a subset of models deployed in GCP central1 |
| 2026-09-21T06:31 | minor | 11 | Model Management API | Metrics degradation in UI and API. **Inference not affected** |
| 2026-09-20T00:19 | major | 55 | Model APIs | Kimi K3 Model API outage |
| 2026-09-14T18:22 | minor | 45 | Dedicated Inference | Elevated errors for models in a single India-based cluster |
| 2026-09-14T09:21 | minor | 42 | Model APIs | Partial outage on Kimi K3 model API inference (non-US only) |
| 2026-09-09T10:42 | minor | 6 | Model APIs | Partial outage on Nemotron Ultra Model API. **Dedicated Inference is not affected** |
| 2026-08-30T23:38 | major | 24 | Dedicated Inference | Elevated inference 500s for models in a single US-based cluster |
| 2026-08-27T14:17 | minor | 14 | Dedicated Inference | Elevated errors for models in a single US cluster due to provider outage |
| 2026-08-25T09:17 | minor | 41 | Model APIs | Elevated errors for deepseek-ai/DeepSeek-V4-Flash-0731 on Model APIs. **Dedicated Inference is not affected** |
| 2026-08-25T05:34 | minor | 41 | Dedicated Inference | Elevated inference 500s for models in an EU cluster due to provider outage |
| 2026-08-18T18:23 | minor | 37 | Model APIs | Elevated errors for moonshotai/Kimi-K3 for US-pinned traffic on Model APIs. **Dedicated Inference is not affec |
| 2026-08-18T12:04 | minor | 77 | Model APIs | Elevated errors for moonshotai/Kimi-K3 for US-pinned traffic on Model APIs. **Dedicated Inference is not affec |
| 2026-08-18T10:24 | minor | 12 | Model APIs | Elevated errors for moonshotai/Kimi-K3 for US-pinned traffic on Model APIs. **Dedicated Inference is not affec |
| 2026-08-18T09:27 | minor | 48 | Model APIs | Elevated errors for moonshotai/Kimi-K3 for US-pinned traffic on Model APIs. **Dedicated Inference is not affec |
| 2026-08-17T09:56 | minor | 46 | Model APIs | Elevated errors for moonshotai/Kimi-K3 for US-pinned traffic |
| 2026-08-17T06:11 | minor | 24 | Model Management API, Web Application | Metrics degradation in UI and API. **Inference not affected** |
| 2026-08-01T16:57 | minor | 43 | Dedicated Inference | Elevated inference 502s for a subset of models in a single US cluster |
| 2026-07-31T16:52 | minor | 29 | Dedicated Inference | Elevated inference 502s for a subset of models in a single US cluster |
| 2026-07-31T09:46 | minor | 12 | Dedicated Inference | Slower than usual scale-ups for B200s |
| 2026-07-22T10:49 | minor | 33 | Dedicated Inference | Elevated inference failures for models in an EU cluster |
| 2026-07-22T10:45 | minor | 19 | Dedicated Inference | Slower than usual scale-ups in 1 us-central cluster |
| 2026-07-18T15:40 | major | 32 | Model APIs | GLM 5.2 Model API partial outage due to provider network failure |
| 2026-07-17T17:22 | minor | 6 | Dedicated Inference | Elevated inference errors in 1 Canada cluster due to provider network outage |
| 2026-07-16T02:06 | minor | 79 | Model Management API, Web Application | Elevated errors in accessing the Baseten UI. **Inference is not affected** |
| 2026-07-12T17:04 | major | 127 | Model APIs | Partial Outage on Model APIs |
| 2026-07-09T07:07 | minor | 14 | Dedicated Inference | Elevated inference 500s for models deployed in 1 US-east cluster |
| 2026-07-08T09:50 | minor | 115 | Model Management API | Metrics degradation in UI and API. **Inference not affected** |
| 2026-07-06T14:08 | minor | 14 | Dedicated Inference | Elevated inference 500s , network outage in our cloud provider in Delaware |
| 2026-07-02T19:59 | major | 86 | Model APIs | Elevated errors for GLM 5.2 on Model APIs. **Dedicated Inference is not affected** |
| 2026-07-02T17:21 | minor | 16 | Dedicated Inference | Elevated inference 500s for a subset of models deployed in 1 cluster |
| 2026-07-02T15:00 | minor | 74 | Model Management API | Degraded metrics performance in dashboard and API. **Inference is not affected** |
| 2026-07-01T03:30 | major | 59 | Dedicated Inference | Elevated errors in a single EU cluster |
| 2026-06-29T11:26 | minor | 35 | Model APIs | Elevated error rates on GLM 5.2 Model APIs. **Dedicated Inference is not affected** |
| 2026-06-26T23:35 | minor | 15 | Dedicated Inference | Elevated inference 500s for models in 1 cluster due to cloud provider outage |
| 2026-06-26T16:41 | minor | 74 | Model Management API | Elevated model deployment failures. **Inference is not affected** |
| 2026-06-26T15:00 | major | 14 | Dedicated Inference | Elevated errors for dedicated inference in a subset of clusters |
| 2026-06-22T17:10 | minor | 44 | Dedicated Inference, Model Management API | Slower than usual scale-ups. High failure rate for new model deploys. Existing replicas aren't impacted. |
| 2026-06-18T05:46 | minor | 104 | Dedicated Inference, Model APIs | Elevated errors for models in 1 Austin-based cluster affecting some models on B200s |
| 2026-06-16T21:40 | minor | 83 | Dedicated Inference | Elevated errors for models in 1 Sweden-based cluster |
| 2026-06-15T09:14 | minor | 44 | Dedicated Inference | Elevated errors for models in a single EU cloud provider |
| 2026-06-13T11:25 | minor | 44 | Dedicated Inference | Elevated errors for models in a single cloud provider |
| 2026-06-04T19:10 | major | 19 | Dedicated Inference | Elevated errors in a single US-East cluster |
| 2026-06-04T13:53 | minor | 66 | Dedicated Inference | Elevated latencies for a subset of models in a US-East cluster |
| 2026-06-03T07:56 | minor | 135 | Dedicated Inference | Slower than usual scale-ups for some models using H100s |
| 2026-05-29T12:31 | minor | 33 | Dedicated Inference | Elevated async inference errors in a single cluster |
| 2026-05-26T09:21 | minor | 14 | Dedicated Inference | Slower than usual scale-ups in 1 India cluster |

## deepinfra: no Statuspage JSON

No Statuspage JSON available.

## nebius: Nebius (https://status.nebius.com)

Components: 161 total, 7 groups, 154 leaf. Page updated 2026-09-29T18:06:51.299Z.

Groups: EU-NORTH1, EU-NORTH2, EU-WEST1, EU-WEST2, UK-SOUTH1, US-CENTRAL1, ME-WEST1

Leaf component names: API (x7), Audit Logs (x7), Billing (x7), Compute Cloud (x7), Container Registry (x7), Identity and Access Management (x7), Logging (x7), Managed Service for Kubernetes® (x7), Managed Service for MLflow (x7), Managed Service for PostgreSQL® (x7), Managed Service for SkyPilot (x7), Managed Soperator (x7), Management Console (x7), Marketplace (x7), Monitoring (x7), Mysterybox (x7), Network Block Storage (x7), Object Storage (x7), Serverless AI (x7), Standalone Applications (x7), Token Factory (x7), Virtual Private Cloud (Networking) (x7)

Incidents returned: 50 (oldest 2026-02-18). Window end: 2026-09-29T18:22:40Z.

### Last 30 days

Incidents: 9 (major: 7, minor: 1, none: 1). Resolved incident-minutes summed across incidents: 2191.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| Managed Service for SkyPilot | 1 | 1473 | 1 | 1473 | 96.589% |
| Object Storage | 1 | 297 | 1 | 297 | 99.313% |
| Compute Cloud | 3 | 259 | 2 | 235 | 99.456% |
| Virtual Private Cloud (Networking) | 2 | 207 | 2 | 207 | 99.522% |
| Monitoring | 1 | 89 | 1 | 89 | 99.795% |
| Identity and Access Management | 1 | 58 | 0 | 0 | 100.000% |
| Managed Service for Kubernetes® | 1 | 15 | 1 | 15 | 99.965% |
| (no component tagged) | 1 | 0 | 1 | 0 | 100.000% |

### Last 90 days

Incidents: 19 (major: 14, minor: 3, none: 2). Resolved incident-minutes summed across incidents: 4004.

| Component | Incidents | Minutes | Major incidents | Major minutes | Availability if major minutes were full downtime |
| --- | --- | --- | --- | --- | --- |
| Managed Service for SkyPilot | 3 | 2860 | 3 | 2860 | 97.794% |
| Compute Cloud | 8 | 1943 | 6 | 1841 | 98.580% |
| Object Storage | 4 | 1786 | 4 | 1786 | 98.622% |
| Virtual Private Cloud (Networking) | 5 | 1618 | 5 | 1618 | 98.751% |
| Token Factory | 3 | 1490 | 3 | 1490 | 98.851% |
| Managed Service for Kubernetes® | 3 | 1401 | 3 | 1401 | 98.919% |
| Managed Service for MLflow | 2 | 1386 | 2 | 1386 | 98.931% |
| Managed Service for PostgreSQL® | 2 | 1386 | 2 | 1386 | 98.931% |
| Serverless AI | 2 | 1386 | 2 | 1386 | 98.931% |
| Monitoring | 4 | 311 | 4 | 311 | 99.760% |
| Logging | 2 | 197 | 2 | 197 | 99.848% |
| Identity and Access Management | 2 | 151 | 1 | 93 | 99.928% |
| Standalone Applications | 2 | 93 | 1 | 93 | 99.928% |
| API | 1 | 93 | 1 | 93 | 99.928% |
| Audit Logs | 1 | 93 | 1 | 93 | 99.928% |
| Billing | 1 | 93 | 1 | 93 | 99.928% |
| Container Registry | 1 | 93 | 1 | 93 | 99.928% |
| Managed Soperator | 1 | 93 | 1 | 93 | 99.928% |
| Management Console | 1 | 93 | 1 | 93 | 99.928% |
| Marketplace | 1 | 93 | 1 | 93 | 99.928% |
| Mysterybox | 1 | 93 | 1 | 93 | 99.928% |
| Network Block Storage | 1 | 93 | 1 | 93 | 99.928% |
| (no component tagged) | 3 | 0 | 2 | 0 | 100.000% |

### Incident log (most recent 50)

| Created (UTC) | Impact | Minutes | Components | Title |
| --- | --- | --- | --- | --- |
| 2026-09-23T05:20 | major | 192 | Compute Cloud, Virtual Private Cloud (Networking) | Network issues in eu-west2 |
| 2026-09-22T08:55 | major | 0 |  | Object storage unavailable in eu-west1 |
| 2026-09-17T16:26 | major | 43 | Compute Cloud | Compute services are partially unavailable for customers |
| 2026-09-17T10:46 | none | 58 | Identity and Access Management | Resuming IAM accounts is unavailable |
| 2026-09-16T16:52 | major | 89 | Monitoring | [eu-west1] Metrics for resources in this region are partially unavailable |
| 2026-09-16T10:45 | major | 297 | Object Storage | [us-central1] Object Storage is partially unavailable |
| 2026-09-14T15:00 | major | 1473 | Managed Service for SkyPilot | Managed Service for SkyPilot: cluster creation and update requests failing in eu-north1 |
| 2026-09-09T12:17 | minor | 24 | Compute Cloud | Unstable compute VM create |
| 2026-09-01T16:11 | major | 15 | Managed Service for Kubernetes®, Virtual Private Cloud (Networking) | Connectivity issues for newly created worker nodes |
| 2026-08-19T10:43 | major | 1293 | Compute Cloud, Managed Service for Kubernetes®, Managed Service for... | Region us-central1 partial degradation |
| 2026-08-17T11:00 | minor | 0 |  | Issues logging to the Management Console |
| 2026-08-15T18:25 | major | 197 | Compute Cloud | Partial InfiniBand unavailability |
| 2026-08-12T13:30 | major | 26 | Monitoring, Virtual Private Cloud (Networking) | External VPC connectivity issues |
| 2026-08-05T14:27 | none | 78 | Compute Cloud | Creation of new VMs is broken |
| 2026-07-27T18:30 | major | 93 | API, Audit Logs, Billing, Compute Cloud, Container Registry, Identi... | Network issues |
| 2026-07-22T03:00 | major | 0 |  | [eu-north1] Network timeouts affecting multiple services |
| 2026-07-14T22:10 | major | 22 | Compute Cloud | InfiniBand switch failure affecting GPU workloads in the eu-north1-c fabric in the eu-north1 region |
| 2026-07-03T14:50 | minor | 0 | Standalone Applications | Managed SkyPilot OIDC Login is unavailable |
| 2026-07-01T22:33 | major | 104 | Logging, Monitoring, Object Storage, Token Factory | Monitoring, Object Storage and Token Factory services are partially unavailable |
| 2026-06-30T13:24 | minor | 4 | Compute Cloud, Network Block Storage | New virtual machines are not being created |
| 2026-06-24T14:08 | major | 97 | Object Storage | Object Storage service partially unavailable in US-CENTRAL1 region |
| 2026-06-16T20:02 | minor | 32 | Compute Cloud | One InfiniBand switch failure |
| 2026-06-15T18:27 | minor | 21 | Virtual Private Cloud (Networking) | Network Connectivity Issues |
| 2026-06-10T20:56 | none | 153 | Compute Cloud | Compute instances startup issues |
| 2026-06-09T10:30 | minor | -175 |  | Some public IPs unreachable in eu-north1 |
| 2026-06-04T09:46 | major | 88 | Logging, Monitoring, Object Storage | Network Connectivity Issues |
| 2026-06-02T10:53 | minor | 1453 | Virtual Private Cloud (Networking) | Unable to allocate new public IPv4 addresses in eu-north1 |
| 2026-05-29T21:22 | none | -58 |  | Power issues |
| 2026-05-19T13:45 | minor | 115 | Compute Cloud | Unable to perform operations on a small subset of virtual machines |
| 2026-05-13T18:45 | minor | 140 | Compute Cloud | InfiniBand performance degradation |
| 2026-05-07T21:03 | none | 24 | Management Console | Nebius console is unavailable |
| 2026-05-06T12:39 | major | 1146 | Managed Service for Kubernetes® | Managed Kubernetes operations can take longer than expected |
| 2026-04-29T15:36 | major | 989 | Token Factory | Partial unavailability of external models in Token Factory |
| 2026-04-24T09:46 | minor | 43 | Token Factory | Partial degradation of Dedicated Endpoints in Token Factory |
| 2026-04-20T07:26 | minor | 1549 | Token Factory | TokenFactory DataLab unavailability |
| 2026-04-20T08:05 | minor | 25 | Monitoring | Metrics for VMs are unavailable |
| 2026-04-15T08:50 | minor | 96 | Token Factory | TokenFactory , Some Serverless Models Partially Unavailable in us-central1 Region |
| 2026-04-10T02:00 | minor | 0 |  | Degraded logs, metrics and audit trails availability |
| 2026-04-07T11:50 | minor | 74 | Token Factory | Observability data partially unavailable for Dedicated Endpoints in TokenFactory |
| 2026-04-01T13:58 | minor | 60 | Identity and Access Management | Slower project and tenant creation |
| 2026-03-26T10:20 | major | 36 | Managed Service for Kubernetes® | Managed k8s is partially unavailable for customers |
| 2026-03-24T23:30 | major | 0 |  | Storage Metrics Ingestion Failure |
| 2026-03-23T20:15 | major | 87 | Token Factory | Observability data partially unavailable in TokenFactory |
| 2026-03-10T15:47 | major | 542 | Compute Cloud, Managed Service for Kubernetes®, Managed Service for... | Power issues during planned maintenance |
| 2026-03-05T17:49 | minor | 42 | Compute Cloud | Some VMs scheduling can take more than 45 minutes |
| 2026-03-02T18:45 | major | 77 | Compute Cloud | Power issues in us-central1 |
| 2026-02-26T14:40 | major | 616 | Compute Cloud, Managed Service for Kubernetes®, Managed Service for... | Power issues in eu-north1 |
| 2026-02-20T22:35 | major | 55 | API, Audit Logs, Billing, Compute Cloud, Container Registry, Identi... | Network issues in us-central1 |
| 2026-02-18T18:26 | major | 1294 | Token Factory | Batch inference unavailability in Token Factory |
| 2026-02-18T13:26 | major | 185 | Managed Service for Kubernetes® | Partial unavailability of Managed Kubernetes LoadBalancers |

