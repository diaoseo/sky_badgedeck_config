#!/usr/bin/env python3
# purge jsDelivr CDN cache for manifest.json + every file listed in it.
# Run from repo root AFTER `git push` so jsDelivr re-fetches fresh content.
import json
import os
import sys
import urllib.error
import urllib.request

REPO = "diaoseo/sky_badgedeck_config"
REF = "main"
MANIFEST = os.path.join("resources", "manifest.json")
PURGE_BASE = "https://purge.jsdelivr.net/gh/%s@%s/" % (REPO, REF)


def main():
    if not os.path.exists(MANIFEST):
        print("purge_cdn: %s not found; run gen_manifest.py first" % MANIFEST)
        return 1
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    # manifest.json itself + every resource it lists (name is relative to resources/)
    paths = ["resources/manifest.json"]
    for entry in manifest.get("files", []):
        name = entry.get("name")
        if name:
            paths.append("resources/" + name)
    rc = 0
    for path in paths:
        url = PURGE_BASE + path
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                print(resp.status, path)
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, path)
            if e.code >= 500:
                rc = 1
        except Exception as e:
            print("FAIL", path, repr(e))
            rc = 1
    print("purge_cdn: done (%d urls)" % len(paths))
    return rc


if __name__ == "__main__":
    sys.exit(main())
