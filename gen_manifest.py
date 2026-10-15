#!/usr/bin/env python3
# regen manifest.json + manifest_hash.php from resources/ (run from repo root)
import hashlib, json, os

RESOURCES = "resources"
OUT_MANIFEST = os.path.join(RESOURCES, "manifest.json")
OUT_GATE = "manifest_hash.php"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


files = []
for root, dirs, names in os.walk(RESOURCES):
    for n in sorted(names):
        full = os.path.join(root, n)
        rel = os.path.relpath(full, RESOURCES).replace(os.sep, "/")
        if rel == "manifest.json":
            continue
        files.append({"name": rel, "size": os.path.getsize(full), "sha256": sha256_file(full)})

files.sort(key=lambda x: x["name"])
text = json.dumps({"bundle_ver": 1, "files": files}, ensure_ascii=False, indent=2) + "\n"
with open(OUT_MANIFEST, "wb") as f:
    f.write(text.encode("utf-8"))

gate = sha256_file(OUT_MANIFEST)
with open(OUT_GATE, "wb") as f:
    f.write((gate + "\n").encode("ascii"))

print("files:", len(files))
print("manifest:", OUT_MANIFEST)
print("gate    :", OUT_GATE, "=", gate)
