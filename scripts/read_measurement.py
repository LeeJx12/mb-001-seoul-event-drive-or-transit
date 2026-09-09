#!/usr/bin/env python3
"""Read MB-001's existing public aggregate counters without writing to them."""

from __future__ import annotations

import argparse
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HISTORY_API = "https://hitscounter.dev/api/history"
BASE = "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events"

# These keys exactly mirror the already-deployed ?metric=<name>-v2 targets.
COUNTERS = (
    ("ddp-2026", "acquisition_view", 1),
    ("ddp-2026", "meaningful_page_use", 0),
    ("ddp-2026", "result_action_map", 0),
    ("ddp-2026", "result_action_official", 0),
    ("ddp-2026", "result_action_transit", 0),
    ("seoripul-2026", "acquisition_view", 1),
    ("seoripul-2026", "meaningful_page_use", 0),
    ("seoripul-2026", "result_action_parking", 0),
    ("seoripul-2026", "result_action_official", 0),
    ("seoripul-2026", "result_action_transit", 0),
)


def target_url(page: str, metric: str) -> str:
    return f"{BASE}/{page}/?metric={metric}-v2"


def read_url(target: str) -> str:
    return f"{HISTORY_API}?{urlencode({'url': target})}"


def read_counter(page: str, metric: str, baseline: int) -> dict:
    target = target_url(page, metric)
    request = Request(read_url(target), headers={"User-Agent": "mb-001-read-only-checkpoint/1"})
    with urlopen(request, timeout=15) as response:
        payload = json.load(response)
    total = int(payload["total_hits"])
    return {
        "page": page,
        "metric": metric,
        "target": target,
        "read_url": read_url(target),
        "total": total,
        "baseline": baseline,
        "net": max(0, total - baseline),
        "history": payload["history"],
    }


def summarize(rows: list[dict]) -> dict:
    views = sum(row["net"] for row in rows if row["metric"] == "acquisition_view")
    meaningful = sum(row["net"] for row in rows if row["metric"] == "meaningful_page_use")
    actions = sum(row["net"] for row in rows if row["metric"].startswith("result_action_"))
    return {
        "acquisition_views": views,
        "meaningful_page_uses": meaningful,
        "result_actions": actions,
        "result_action_rate": actions / views if views else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()
    rows = [read_counter(*counter) for counter in COUNTERS]
    output = {"counters": rows, "combined_net": summarize(rows)}
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    print("page\tmetric\ttotal\tbaseline\tnet")
    for row in rows:
        print(f"{row['page']}\t{row['metric']}\t{row['total']}\t{row['baseline']}\t{row['net']}")
    print("\ncombined net")
    for key, value in output["combined_net"].items():
        print(f"{key}: {value:.2%}" if key.endswith("_rate") else f"{key}: {value}")


if __name__ == "__main__":
    main()
