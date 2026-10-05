# fineprint

Gold-standard translation of Hugging Face dataset licenses into ODRL.
Private working repo: natural-language license texts, and two independent
ODRL annotations of each.

- `docs/`: license census (report, CSV, policy-presence figure)
- `licenses/`: license texts (`MANUAL.md` lists the ones to resolve by hand)
- `annotator-1-meem/`, `annotator-2-beatriz/`: one `<hf-id>.jsonld` per license

Workflow: Tier 1 (15 licenses) is annotated by both annotators first, then
Tier 2. Annotate from the license text only, not from the automatic mapping,
and do not read the other annotator's folder until both are done.

Note: tldrlegal.com content must not be copied into this repo.
