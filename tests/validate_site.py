#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree
import importlib.util
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/",
    "/seoul-events/ddp-2026/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/ddp-2026/",
    "/seoul-events/seoripul-2026/": "https://leejx12.github.io/mb-001-seoul-event-drive-or-transit/seoul-events/seoripul-2026/",
}
INDEXNOW_KEY = "7f1b2d8c4a6e4093b5c7d9e1f3a8b2c4"


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonicals = []
        self.title = False
        self.description = None
        self.robots = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append((attrs["href"], attrs.get("class", "")))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content")
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots = attrs.get("content")
        if tag == "title":
            self.title = True


def local_target(page_path, href):
    parsed = urlparse(href)
    target = page_path.parent / parsed.path
    if parsed.path.endswith("/"):
        target /= "index.html"
    return target.resolve()


errors = []
for route, canonical in EXPECTED.items():
    path = ROOT / route.strip("/") / "index.html" if route != "/" else ROOT / "index.html"
    source = path.read_text(encoding="utf-8")
    doc = Document()
    doc.feed(source)
    if doc.canonicals != [canonical]:
        errors.append(f"{path}: canonical {doc.canonicals!r}")
    if not doc.title:
        errors.append(f"{path}: missing title")
    if not doc.description:
        errors.append(f"{path}: missing description")
    if not doc.robots or "index" not in doc.robots:
        errors.append(f"{path}: missing index robots directive")
    for href, _ in doc.links:
        parsed = urlparse(href)
        if parsed.scheme or href.startswith(("#", "mailto:", "tel:")):
            continue
        if not local_target(path, href).exists():
            errors.append(f"{path}: broken internal link {href}")

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    try:
        schemas = [json.loads(block) for block in blocks]
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON-LD: {exc}")
        schemas = []
    if len(schemas) != 1:
        errors.append(f"{path}: expected one JSON-LD block")
    elif route == "/":
        if schemas[0].get("@type") != "CollectionPage" or schemas[0].get("mainEntity", {}).get("numberOfItems") != 2:
            errors.append(f"{path}: invalid bounded collection schema")
    else:
        schema = schemas[0]
        for field in ("name", "startDate", "endDate", "location", "organizer", "offers"):
            if field not in schema:
                errors.append(f"{path}: event schema missing {field}")
        if schema.get("@type") not in {"Event", "Festival"} or schema.get("url") != canonical:
            errors.append(f"{path}: event schema type or URL mismatch")
        if not any("source" in classes.split() for _, classes in doc.links):
            errors.append(f"{path}: missing visible official source attribution")
        for metric in ("acquisition_view", "meaningful_page_use", "result_action_", "acquisition_source_"):
            if metric not in source:
                errors.append(f"{path}: missing event semantic {metric}")
        for source_name in ("search_google", "search_naver", "search_bing", "search_daum", "owned_home", "owned_related"):
            if source_name not in source:
                errors.append(f"{path}: missing allow-listed source {source_name}")
        if "encodeURIComponent(document.referrer)" in source:
            errors.append(f"{path}: full referrer must never be transmitted")
        if 'href="../../"' not in source or "?src=owned-related" not in source:
            errors.append(f"{path}: missing bounded internal discovery links")

root_source = (ROOT / "index.html").read_text(encoding="utf-8")
if root_source.count("?src=owned-home") != 2:
    errors.append("root: both event links must carry owned-home attribution")

sitemap = ElementTree.parse(ROOT / "sitemap.xml")
namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
sitemap_rows = {
    node.findtext("s:loc", namespaces=namespace): node.findtext("s:lastmod", namespaces=namespace)
    for node in sitemap.findall("s:url", namespace)
}
if sitemap_rows != {url: "2026-09-09" for url in EXPECTED.values()}:
    errors.append(f"sitemap URLs/lastmod mismatch: {sitemap_rows!r}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
if "Allow: /" not in robots or f"Sitemap: {EXPECTED['/']}sitemap.xml" not in robots:
    errors.append("robots.txt does not allow crawl and expose the canonical sitemap")

key_path = ROOT / f"{INDEXNOW_KEY}.txt"
if not key_path.exists() or key_path.read_text(encoding="utf-8").strip() != INDEXNOW_KEY:
    errors.append("IndexNow key file missing or mismatched")

measurement_path = ROOT / "scripts" / "read_measurement.py"
spec = importlib.util.spec_from_file_location("read_measurement", measurement_path)
measurement = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measurement)
expected_funnel = {
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
expected_sources = {
    (page, metric, 0)
    for page in ("ddp-2026", "seoripul-2026")
    for metric in measurement.SOURCE_METRICS
}
if set(measurement.COUNTERS) != expected_funnel | expected_sources:
    errors.append("measurement helper counter inventory or baseline drifted")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(
    f"Validated {len(EXPECTED)} HTML pages and {len(measurement.COUNTERS)} measurement keys: "
    "crawlability, canonicals, structured data, official sources, internal links, attribution, sitemap, and baselines OK"
)
