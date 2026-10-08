"""Submit a sibling site's URLs to IndexNow (Bing, Yandex, Seznam, Naver).

IndexNow only accepts a submission after the key file is deployed and reachable,
so run this AFTER `wrangler pages deploy`. It re-reads sitemap.xml, so newly
added pages are picked up automatically.

Usage:  python build.py && (deploy) && python submit_indexnow.py
"""
import json
import pathlib
import re
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT / "site"

key = (ROOT / "indexnow-key.txt").read_text(encoding="utf-8").strip()
data = json.loads((ROOT / "data" / "brands.json").read_text(encoding="utf-8"))
base = data["site"]["base_url"].rstrip("/")
host = base.split("//", 1)[1]

urls = re.findall(r"<loc>([^<]+)</loc>", (SITE / "sitemap.xml").read_text(encoding="utf-8"))
if not urls:
    raise SystemExit("NO URLS IN sitemap.xml - run build.py first")

# The key file has to be live before the endpoint will accept the submission;
# check it here so a failed submit is reported as the real cause.
probe = f"{base}/{key}.txt"
# ::RULE{Cloudflare 会 403 掉 python-urllib 的默认 UA，必须显式带 UA}
UA = f"Mozilla/5.0 (compatible; {host}-indexnow/1.0; +{base}/about)"
try:
    req = urllib.request.Request(probe, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        live_key = r.read().decode("utf-8").strip()
except urllib.error.URLError as e:
    raise SystemExit(f"KEY FILE NOT LIVE YET: {probe} ({e}) - deploy first")
if live_key != key:
    raise SystemExit(f"KEY FILE MISMATCH at {probe}: served {live_key!r}, expected {key!r}")

payload = {
    "host": host,
    "key": key,
    "keyLocation": probe,
    "urlList": urls,
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=60) as r:
        print(f"IndexNow: HTTP {r.status} for {len(urls)} urls ({host})")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", "replace")
    raise SystemExit(f"IndexNow FAILED: HTTP {e.code} {e.reason}\n{body}")
