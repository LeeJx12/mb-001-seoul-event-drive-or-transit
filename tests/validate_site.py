#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/",
    "/seoul-events/ddp-2026/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/",
    "/seoul-events/seoripul-2026/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/",
}

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.canonicals = []; self.title = False; self.description = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs: self.links.append(attrs["href"])
        if tag == "link" and attrs.get("rel") == "canonical": self.canonicals.append(attrs.get("href"))
        if tag == "meta" and attrs.get("name") == "description": self.description = attrs.get("content")
        if tag == "title": self.title = True

errors = []
for route, canonical in EXPECTED.items():
    path = ROOT / route.strip("/") / "index.html" if route != "/" else ROOT / "index.html"
    doc = Document(); doc.feed(path.read_text(encoding="utf-8"))
    if doc.canonicals != [canonical]: errors.append(f"{path}: canonical {doc.canonicals!r}")
    if not doc.title: errors.append(f"{path}: missing title")
    if not doc.description: errors.append(f"{path}: missing description")
    for href in doc.links:
        parsed = urlparse(href)
        if parsed.scheme or href.startswith(("#", "mailto:", "tel:")): continue
        target = (path.parent / parsed.path)
        if href.endswith("/"): target /= "index.html"
        if not target.resolve().exists(): errors.append(f"{path}: broken internal link {href}")
    if route != "/":
        source = path.read_text(encoding="utf-8")
        for metric in ("acquisition_view", "meaningful_page_use", "result_action_"):
            if metric not in source: errors.append(f"{path}: missing event semantic {metric}")
        if 'href="../../"' not in source: errors.append(f"{path}: missing internal home link")

measurement_path = ROOT / "scripts" / "read_measurement.py"
spec = importlib.util.spec_from_file_location("read_measurement", measurement_path)
measurement = importlib.util.module_from_spec(spec); spec.loader.exec_module(measurement)
expected_counters = {
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
}
if set(measurement.COUNTERS) != expected_counters:
    errors.append("measurement helper counter inventory or baseline drifted")
for page, metric, _ in measurement.COUNTERS:
    page_source = (ROOT / "seoul-events" / page / "index.html").read_text(encoding="utf-8")
    semantic = metric if not metric.startswith("result_action_") else f'data-k="{metric.removeprefix("result_action_")}"'
    if semantic not in page_source:
        errors.append(f"{page}: measurement helper references undeployed event {metric}")
if errors:
    print("\n".join(errors), file=sys.stderr); raise SystemExit(1)
print(
    f"Validated {len(EXPECTED)} HTML pages and {len(expected_counters)} "
    "measurement keys: canonicals, titles, links, semantics, and baselines OK"
)

