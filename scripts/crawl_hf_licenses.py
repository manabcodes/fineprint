#!/usr/bin/env python3
"""
Fetch ALL public datasets from the Hugging Face Hub and rank licenses.

Phase 1 (crawl):  streams every dataset's metadata to hf_datasets.jsonl.
                  Safe to Ctrl-C or crash; re-running resumes (it re-pages
                  through already-saved records but skips writing them again).
Phase 2 (tally):  reads the JSONL and writes hf_license_stats.csv + prints top N.

Usage:
    pip install -U huggingface_hub
    export HF_TOKEN=hf_...        # recommended, avoids tight rate limits
    python crawl_hf_licenses.py
    python crawl_hf_licenses.py --tally-only   # skip crawling, reuse the JSONL
"""
import argparse
import csv
import inspect
import json
import os
import sys
import time
from collections import Counter, defaultdict

from huggingface_hub import HfApi

OUT_JSONL = "hf_datasets.jsonl"
OUT_CSV = "hf_license_stats.csv"
EXPAND = ["tags", "downloads", "downloadsAllTime", "likes", "createdAt"]
MAX_CONSECUTIVE_FAILURES = 8


def load_seen_ids(path):
    seen = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    seen.add(json.loads(line)["id"])
                except Exception:
                    pass  # ignore a truncated last line from a crash
    return seen


def crawl():
    api = HfApi(token=os.environ.get("HF_TOKEN"))
    seen = load_seen_ids(OUT_JSONL)
    print(f"Already have {len(seen):,} datasets on disk.", flush=True)

    failures = 0
    start = time.time()
    new_count = 0

    while True:
        try:
            # newest-first is stable enough; dedupe by id handles any shifting
            kwargs = dict(sort="created_at", expand=EXPAND)
            # Older huggingface_hub versions accept direction=-1; newer ones removed it.
            if "direction" in inspect.signature(api.list_datasets).parameters:
                kwargs["direction"] = -1
            it = api.list_datasets(**kwargs)
            with open(OUT_JSONL, "a", encoding="utf-8") as out:
                scanned = 0
                for ds in it:
                    scanned += 1
                    if ds.id in seen:
                        continue
                    seen.add(ds.id)
                    out.write(json.dumps({
                        "id": ds.id,
                        "tags": ds.tags or [],
                        "downloads": ds.downloads or 0,
                        "downloads_all_time": getattr(ds, "downloads_all_time", None) or 0,
                        "likes": ds.likes or 0,
                        "created_at": ds.created_at.isoformat() if ds.created_at else None,
                    }) + "\n")
                    new_count += 1
                    failures = 0
                    if new_count % 10_000 == 0:
                        out.flush()
                        rate = new_count / (time.time() - start)
                        print(f"  +{new_count:,} new (total {len(seen):,}) "
                              f"~{rate:,.0f}/s", flush=True)
            break  # finished the full listing without error
        except KeyboardInterrupt:
            print("\nInterrupted. Progress saved; re-run to resume.")
            sys.exit(1)
        except (TypeError, ValueError, AttributeError, ImportError):
            raise  # code/version problems won't fix themselves on retry
        except Exception as e:
            failures += 1
            if failures > MAX_CONSECUTIVE_FAILURES:
                print(f"Too many consecutive failures, giving up: {e}")
                sys.exit(1)
            wait = min(300, 5 * 2 ** failures)
            print(f"Error ({e!r}). Retry {failures}/{MAX_CONSECUTIVE_FAILURES} "
                  f"in {wait}s...", flush=True)
            time.sleep(wait)

    print(f"Crawl complete: {len(seen):,} datasets on disk "
          f"({time.time() - start:,.0f}s this run).")


def tally(top_n=30):
    n_ds = Counter()
    n_ds_first = Counter()          # only the first declared license per dataset
    dl_30d = defaultdict(int)
    dl_all = defaultdict(int)
    likes = defaultdict(int)
    total = 0

    with open(OUT_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            total += 1
            lics = [t.split(":", 1)[1] for t in r["tags"] if t.startswith("license:")]
            if not lics:
                lics = ["(none declared)"]
            n_ds_first[lics[0]] += 1
            for lic in lics:
                n_ds[lic] += 1
                dl_30d[lic] += r["downloads"]
                dl_all[lic] += r["downloads_all_time"]
                likes[lic] += r["likes"]

    rows = [{
        "license": lic,
        "datasets": n_ds[lic],
        "datasets_first_license_only": n_ds_first.get(lic, 0),
        "downloads_30d": dl_30d[lic],
        "downloads_all_time": dl_all[lic],
        "likes": likes[lic],
    } for lic in n_ds]
    rows.sort(key=lambda r: r["datasets"], reverse=True)

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\n{total:,} datasets analysed. Full table -> {OUT_CSV}\n")
    print(f"{'license':28}{'datasets':>10}{'dl_30d':>16}{'dl_all_time':>18}{'likes':>10}")
    for r in rows[:top_n]:
        print(f"{r['license']:28}{r['datasets']:>10,}{r['downloads_30d']:>16,}"
              f"{r['downloads_all_time']:>18,}{r['likes']:>10,}")

    for key, label in [("downloads_30d", "30-day downloads"),
                       ("downloads_all_time", "all-time downloads")]:
        print(f"\nTop 10 by {label}:")
        for r in sorted(rows, key=lambda r: r[key], reverse=True)[:10]:
            print(f"  {r['license']:28}{r[key]:>18,}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tally-only", action="store_true")
    p.add_argument("--top", type=int, default=30)
    args = p.parse_args()
    if not args.tally_only:
        crawl()
    tally(args.top)
