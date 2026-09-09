# MB-001 aggregate measurement reads

This document covers only the two existing production event pages and their already-deployed `hitscounter.dev` targets. It does not add or change instrumentation.

## Read-only procedure

Run this from a clean product checkout:

```sh
python scripts/read_measurement.py
python scripts/read_measurement.py --json
```

The helper sends `GET` requests only to `https://hitscounter.dev/api/history?url=<encoded-target>`. The public human-readable equivalent is `https://hitscounter.dev/history?url=<encoded-target>`. The API returns `total_hits`, `today_hits`, and daily `history`; unlike `/api/hit`, `/api/history` does not register a hit.

On 2026-09-09 21:14 KST, every target below was read twice consecutively. All ten first and second totals matched, confirming that history reads did not increment any counter. The service's public source also implements `/api/history` with database `SELECT` statements only.

## Exact production keys and baselines

Every target is the canonical page URL plus `?metric=<event>-v2`.

| Page | Event/key suffix | Exact production target | 2026-09-09 total | Subtract at checkpoint |
| --- | --- | --- | ---: | ---: |
| `ddp-2026` | `acquisition_view-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/?metric=acquisition_view-v2` | 1 | 1 |
| `ddp-2026` | `meaningful_page_use-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/?metric=meaningful_page_use-v2` | 0 | 0 |
| `ddp-2026` | `result_action_map-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/?metric=result_action_map-v2` | 0 | 0 |
| `ddp-2026` | `result_action_official-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/?metric=result_action_official-v2` | 0 | 0 |
| `ddp-2026` | `result_action_transit-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/?metric=result_action_transit-v2` | 0 | 0 |
| `seoripul-2026` | `acquisition_view-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/?metric=acquisition_view-v2` | 1 | 1 |
| `seoripul-2026` | `meaningful_page_use-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/?metric=meaningful_page_use-v2` | 0 | 0 |
| `seoripul-2026` | `result_action_parking-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/?metric=result_action_parking-v2` | 0 | 0 |
| `seoripul-2026` | `result_action_official-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/?metric=result_action_official-v2` | 0 | 0 |
| `seoripul-2026` | `result_action_transit-v2` | `https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/?metric=result_action_transit-v2` | 0 | 0 |

The two acquisition hits occurred on 2026-09-06, before the fixed retest window began on 2026-09-07. They are the known operator/deployment-verification baseline, not product demand. No other pre-window hits exist in the readable history.

## 2026-09-21 checkpoint calculation

1. Run `python scripts/read_measurement.py --json` once after the window closes.
2. For each key calculate `net = max(0, total_hits - baseline)`. The helper performs this subtraction.
3. Sum the two net `acquisition_view` values for combined acquisition views.
4. Sum the two net `meaningful_page_use` values for combined meaningful uses.
5. Sum all six net `result_action_*` values for combined result actions.
6. Calculate `result actions / acquisition views`; if views are zero, report the rate as unavailable rather than inferring demand.
7. Apply the unchanged control-plane PASS/ITERATE/STOP thresholds. Keep daily history as the audit trail and report any service/read anomaly as `MEASUREMENT BLOCKED`.

The counter is once-per-browser/page/version, not a verified unique-person measure. Counts are directional aggregate evidence. Do not treat the page load used for live verification as demand; fetch live HTML directly or use a browser profile whose existing localStorage key already prevents another production hit.

## Privacy and cost boundary

Reads require no account, credentials, cookie, identifier, backend, or new vendor. This helper transmits only the already-public exact counter target in a read-only query. Existing browser writes remain unchanged. Incremental and recurring cost is KRW0.
