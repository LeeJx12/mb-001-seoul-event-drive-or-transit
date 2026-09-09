# MB-001 Seoul Event Drive-or-Transit Pages

Static, event-specific Korean guides that help visitors choose between driving and public transit.

## Pages

- [서울라이트 DDP 2026](https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/)
- [서리풀뮤직페스티벌 2026](https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/)

## Local verification

```sh
python3 tests/validate_site.py
python3 scripts/read_measurement.py
python3 -m http.server 8000
```

The production deployment uses GitHub Pages from the `main` branch root and has no recurring infrastructure cost.
The read-only aggregate counter procedure and fixed pre-window baselines are documented in [`docs/MEASUREMENT.md`](docs/MEASUREMENT.md).
