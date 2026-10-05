import csv, json, pathlib, urllib.request

RAW = "https://raw.githubusercontent.com/spdx/license-list-data/main"
get = lambda u: urllib.request.urlopen(u, timeout=30).read().decode("utf-8")

spdx = {l["licenseId"].lower(): l["licenseId"]
        for l in json.loads(get(f"{RAW}/json/licenses.json"))["licenses"]}

# HF ids that differ from SPDX ids. -only/-or-later is a judgment call (see MANUAL.md).
ALIAS = {
 "odbl": "ODbL-1.0", "odc-by": "ODC-By-1.0", "pddl": "PDDL-1.0",
 "c-uda": "C-UDA-1.0", "gfdl": "GFDL-1.3-only",
 "gpl-2.0": "GPL-2.0-only", "gpl-3.0": "GPL-3.0-only",
 "agpl-3.0": "AGPL-3.0-only", "lgpl-2.1": "LGPL-2.1-only",
 "lgpl-3.0": "LGPL-3.0-only", "lgpl-lr": "LGPLLR",
 "eupl-1.1": "EUPL-1.1", "eupl-1.2": "EUPL-1.2",
}
VAGUE = {"other", "unknown", "cc", "gpl", "bsd", "lgpl"}
AMBIGUOUS_VERSION = {"gfdl", "gpl-2.0", "gpl-3.0", "agpl-3.0",
                     "lgpl-2.1", "lgpl-3.0"}

ids = [r["license"] for r in csv.DictReader(open("docs/hf_license_stats.csv", encoding="utf-8-sig"))
       if r["license"] != "(none declared)"]

out, manual = pathlib.Path("licenses"), []
for hf in ids:
    if hf in VAGUE:
        manual.append(f"- `{hf}`: vague label, scope decision needed"); continue
    sid = ALIAS.get(hf) or spdx.get(hf.lower())
    if not sid:
        manual.append(f"- `{hf}`: no SPDX id, fetch text by hand"); continue
    try:
        (out / f"{hf}.txt").write_text(get(f"{RAW}/text/{sid}.txt"), encoding="utf-8")
        if hf in AMBIGUOUS_VERSION:
            manual.append(f"- `{hf}`: fetched as {sid}; HF id has no -only/-or-later, confirm")
    except Exception as e:
        manual.append(f"- `{hf}`: SPDX id {sid} but fetch failed ({e})")

(out / "MANUAL.md").write_text("# Needs manual attention\n\n" + "\n".join(manual) + "\n")
print(f"{len(ids)} ids, {len(list(out.glob('*.txt')))} texts fetched, {len(manual)} flagged")
