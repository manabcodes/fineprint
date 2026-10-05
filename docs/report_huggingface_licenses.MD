# Hugging Face dataset licenses: census and ODRL canonization targets

Prepared for Beatriz Esteves · Meem Arafat Manab · 5 October 2026

## Summary

Hugging Face datasets use 83 distinct license identifiers: 77 specific licenses and 6 vague labels. Each of them needs an ODRL policy built independently for the gold standard, from the license text and not from the automatic mapping that the gold standard is meant to validate.

We crawled all 1,077,443 public datasets on the Hub. Of these, 705,237 (65%) declare no license, and 372,206 declare at least one. The 77 specific licenses cover 89.5% of the licensed datasets and the 6 vague labels (`other`, `unknown`, `cc`, `gpl`, `bsd`, `lgpl`) cover the other 10.5%. Fifteen licenses account for 95% of the datasets that declare a specific license and 96% of those licenses' all-time downloads, which gives a natural first batch for annotation.

The 83 identifiers sit just above the roughly 30 to 80 licenses our project proposal scopes for the gold-standard SPDX to ODRL mapping. The census is over the whole Hub, so the top-10,000 scope of the resource paper will likely contain fewer; we have not measured that yet.

What we need from you: confirm the priority order below, and decide how to treat the AI model licenses, the six vague labels and the unlicensed majority.

## Method

The numbers come from one full crawl of the Hub's public dataset listing, using the `huggingface_hub` Python client, completed in about 9.5 minutes.

For each dataset we recorded its tags, 30-day downloads, all-time downloads, likes and creation date. A dataset's license is the value of its `license:<id>` tag, so these are the licenses authors declared, not verified ones. A dataset with no such tag is counted as having no declared license.

Some datasets declare more than one license. The per-license table below counts a dataset under every license it lists, so its counts add up to slightly more than the number of datasets (847 extra assignments). The shares quoted in the text count each dataset once, under its first license, so they add up to 100%.

Download figures are the Hub's own counters and can include automated pulls, so they indicate relative use rather than unique users.

## Findings

Usage is concentrated in a few licenses, with a long tail behind them. Apache-2.0, MIT and CC BY 4.0 alone account for about 73% of licensed datasets.

| Family | Licenses | Share of licensed datasets | Share of 30-day downloads | Share of all-time downloads |
| --- | ---: | ---: | ---: | ---: |
| Permissive software | 16 | 58.5% | 48.3% | 46.1% |
| Creative Commons | 16 | 24.7% | 32.6% | 32.3% |
| Vague label | 6 | 10.5% | 10.8% | 13.0% |
| AI model, RAIL and custom | 20 | 3.9% | 0.4% | 0.6% |
| Open data and content | 11 | 1.6% | 7.0% | 7.4% |
| Copyleft and weak-copyleft software | 14 | 0.8% | 1.0% | 0.6% |

Four things stand out:

- **Dataset counts and downloads disagree.** The open data and content licenses are 1.6% of licensed datasets but 7.4% of all-time downloads. `gfdl` alone has about 47 million all-time downloads from only 262 datasets. The AI model group is the reverse: 3.9% of datasets but 0.6% of downloads, mostly `openrail` (8,375 datasets).
- **Vague labels are one in ten licensed datasets.** `other` (29,995 datasets) and `unknown` (5,489) cannot be turned into a policy without reading each dataset card or its license text.
- **Creative Commons is the largest family by identifier.** It has 16 identifiers across versions 2.0 to 4.0 and the clause combinations BY, BY-SA, BY-NC, BY-NC-SA, BY-ND and BY-NC-ND. Each version has its own legal text, so each identifier needs its own annotation.
- **The AI model group is large in identifiers, small in use.** Its 20 identifiers include the OpenRAIL variants and the Llama, Gemma and Grok community licenses.

## Nested and dual licenses

Nested (conjunctive) and dual-licensed (disjunctive) cases are where this work gets interesting, because they are where a single-license mapping stops being enough. The census gives a first measure of how often the Hub itself records more than one license, and a clear view of what it cannot tell us.

**What the census shows.**

- At most 847 datasets (about 0.2% of the 372,206 licensed ones) list more than one license tag. The upper bound is exact, because a dataset with three tags adds two extra assignments.
- A few licenses are much more often listed alongside another one than on their own. `gfdl` appears as a non-first license in 180 of its 262 datasets (69%), a pattern consistent with a content license dual-licensed next to a Creative Commons one. After it, the most frequent secondary listings are `cc-by-4.0` (101), `apache-2.0` (80), `cc-by-sa-4.0` (72), `other` (66) and `mit` (65).
- The pool of explicitly multi-licensed datasets is therefore small, in the hundreds. That suits hand-verified gold-standard annotation well. It is probably too small to train on, so at RL scale the nested cases will likely have to be composed from single-license datasets.

**What it cannot show.**

- A list of license tags does not say whether the licenses are alternatives (the user picks one) or cumulative (all apply). Telling a disjunctive case from a conjunctive one needs the dataset card or license text.
- License tags describe a dataset's own declared license. They say nothing about a dataset built by merging others, such as the real nested cases our proposal cites (`GaussianWorld/scene_splat_7k`, `bigcode/the-stack`).
- Which licenses co-occur with which cannot be read from the per-license counts. That needs the per-dataset records from the crawl, which we have on disk and can analyze next.

## The licenses to canonize

All 83 named license identifiers on the Hub are listed below by priority and then by number of datasets. Tier 1 holds the 15 licenses that rank in the top 13 by number of datasets or the top 10 by all-time downloads. Tier 2 holds the other 62 specific licenses, grouped by family. The six vague labels need a decision before they can be annotated.

| HF license ID | Family | Priority | Datasets | Downloads, 30 days | Downloads, all time |
| --- | --- | --- | ---: | ---: | ---: |
| `apache-2.0` | Permissive software | Tier 1 | 141,660 | 35,137,931 | 417,282,016 |
| `mit` | Permissive software | Tier 1 | 70,727 | 27,787,080 | 690,444,719 |
| `cc-by-4.0` | Creative Commons | Tier 1 | 58,236 | 20,391,563 | 292,901,849 |
| `cc-by-nc-4.0` | Creative Commons | Tier 1 | 9,075 | 4,438,610 | 71,110,893 |
| `cc-by-sa-4.0` | Creative Commons | Tier 1 | 8,676 | 4,351,216 | 124,910,617 |
| `openrail` | AI model, RAIL and custom | Tier 1 | 8,375 | 218,404 | 6,480,347 |
| `cc0-1.0` | Creative Commons | Tier 1 | 5,789 | 3,228,911 | 49,648,196 |
| `cc-by-nc-sa-4.0` | Creative Commons | Tier 1 | 5,087 | 5,703,794 | 124,049,540 |
| `odbl` | Open data and content | Tier 1 | 2,488 | 227,540 | 1,822,590 |
| `odc-by` | Open data and content | Tier 1 | 2,058 | 6,101,294 | 121,783,275 |
| `cc-by-nc-nd-4.0` | Creative Commons | Tier 1 | 1,712 | 552,867 | 10,342,989 |
| `afl-3.0` | Permissive software | Tier 1 | 1,583 | 69,764 | 1,772,896 |
| `creativeml-openrail-m` | AI model, RAIL and custom | Tier 1 | 1,453 | 65,005 | 1,408,236 |
| `cc-by-sa-3.0` | Creative Commons | Tier 1 | 1,302 | 2,853,836 | 64,283,161 |
| `gfdl` | Open data and content | Tier 1 | 262 | 2,317,394 | 47,066,818 |
| `cc-by-3.0` | Creative Commons | Tier 2 | 505 | 584,600 | 11,223,095 |
| `cc-by-2.0` | Creative Commons | Tier 2 | 423 | 121,418 | 10,306,895 |
| `cc-by-nd-4.0` | Creative Commons | Tier 2 | 370 | 83,382 | 6,411,281 |
| `cc-by-nc-2.0` | Creative Commons | Tier 2 | 292 | 70,671 | 983,216 |
| `cc-by-nc-sa-3.0` | Creative Commons | Tier 2 | 244 | 117,155 | 6,089,989 |
| `cc-by-nc-3.0` | Creative Commons | Tier 2 | 191 | 187,759 | 4,884,147 |
| `cc-by-2.5` | Creative Commons | Tier 2 | 146 | 46,466 | 1,356,936 |
| `cc-by-nc-nd-3.0` | Creative Commons | Tier 2 | 128 | 9,810 | 127,770 |
| `cc-by-nc-sa-2.0` | Creative Commons | Tier 2 | 114 | 9,240 | 125,396 |
| `cdla-permissive-2.0` | Open data and content | Tier 2 | 416 | 182,453 | 2,693,236 |
| `c-uda` | Open data and content | Tier 2 | 296 | 48,360 | 818,325 |
| `cdla-sharing-1.0` | Open data and content | Tier 2 | 248 | 152,456 | 2,600,345 |
| `pddl` | Open data and content | Tier 2 | 177 | 20,167 | 353,007 |
| `etalab-2.0` | Open data and content | Tier 2 | 152 | 52,815 | 1,237,614 |
| `cdla-permissive-1.0` | Open data and content | Tier 2 | 91 | 15,005 | 80,696 |
| `openmdw-1.0` | Open data and content | Tier 2 | 31 | 213 | 2,226 |
| `openmdw-1.1` | Open data and content | Tier 2 | 22 | 20,831 | 194,707 |
| `artistic-2.0` | Permissive software | Tier 2 | 848 | 11,720 | 210,037 |
| `bsd-3-clause` | Permissive software | Tier 2 | 796 | 198,565 | 2,030,271 |
| `bsd-2-clause` | Permissive software | Tier 2 | 567 | 35,623 | 493,882 |
| `bsl-1.0` | Permissive software | Tier 2 | 408 | 3,439 | 48,456 |
| `wtfpl` | Permissive software | Tier 2 | 394 | 76,512 | 517,449 |
| `unlicense` | Permissive software | Tier 2 | 392 | 39,286 | 1,035,815 |
| `bsd-3-clause-clear` | Permissive software | Tier 2 | 214 | 10,658 | 105,542 |
| `ecl-2.0` | Permissive software | Tier 2 | 92 | 5,269 | 62,239 |
| `postgresql` | Permissive software | Tier 2 | 48 | 1,550 | 28,289 |
| `zlib` | Permissive software | Tier 2 | 38 | 938 | 14,422 |
| `isc` | Permissive software | Tier 2 | 35 | 619 | 11,706 |
| `ncsa` | Permissive software | Tier 2 | 26 | 203 | 14,550 |
| `ofl-1.1` | Permissive software | Tier 2 | 22 | 445 | 6,511 |
| `gpl-3.0` | Copyleft and weak-copyleft software | Tier 2 | 1,377 | 1,029,512 | 8,643,357 |
| `agpl-3.0` | Copyleft and weak-copyleft software | Tier 2 | 654 | 195,520 | 3,462,401 |
| `gpl-2.0` | Copyleft and weak-copyleft software | Tier 2 | 170 | 39,722 | 492,128 |
| `lgpl-3.0` | Copyleft and weak-copyleft software | Tier 2 | 141 | 12,049 | 275,769 |
| `mpl-2.0` | Copyleft and weak-copyleft software | Tier 2 | 86 | 5,742 | 175,410 |
| `eupl-1.1` | Copyleft and weak-copyleft software | Tier 2 | 68 | 2,498 | 52,884 |
| `ms-pl` | Copyleft and weak-copyleft software | Tier 2 | 53 | 2,609 | 126,354 |
| `eupl-1.2` | Copyleft and weak-copyleft software | Tier 2 | 48 | 5,062 | 52,398 |
| `epl-1.0` | Copyleft and weak-copyleft software | Tier 2 | 44 | 145 | 2,782 |
| `lppl-1.3c` | Copyleft and weak-copyleft software | Tier 2 | 43 | 175 | 3,537 |
| `lgpl-2.1` | Copyleft and weak-copyleft software | Tier 2 | 42 | 941 | 13,610 |
| `osl-3.0` | Copyleft and weak-copyleft software | Tier 2 | 40 | 1,572 | 20,462 |
| `epl-2.0` | Copyleft and weak-copyleft software | Tier 2 | 33 | 825 | 13,167 |
| `lgpl-lr` | Copyleft and weak-copyleft software | Tier 2 | 30 | 546 | 10,601 |
| `bigscience-bloom-rail-1.0` | AI model, RAIL and custom | Tier 2 | 1,057 | 36,927 | 667,703 |
| `bigscience-openrail-m` | AI model, RAIL and custom | Tier 2 | 1,022 | 15,200 | 1,980,733 |
| `bigcode-openrail-m` | AI model, RAIL and custom | Tier 2 | 988 | 9,877 | 176,219 |
| `llama2` | AI model, RAIL and custom | Tier 2 | 350 | 12,755 | 283,169 |
| `llama3.1` | AI model, RAIL and custom | Tier 2 | 273 | 17,745 | 345,765 |
| `llama3` | AI model, RAIL and custom | Tier 2 | 266 | 19,741 | 455,087 |
| `gemma` | AI model, RAIL and custom | Tier 2 | 177 | 4,552 | 63,160 |
| `llama3.2` | AI model, RAIL and custom | Tier 2 | 170 | 3,860 | 119,953 |
| `openrail++` | AI model, RAIL and custom | Tier 2 | 126 | 40,775 | 705,772 |
| `llama3.3` | AI model, RAIL and custom | Tier 2 | 99 | 11,318 | 164,825 |
| `fair-noncommercial-research-license` | AI model, RAIL and custom | Tier 2 | 63 | 55,941 | 470,634 |
| `llama4` | AI model, RAIL and custom | Tier 2 | 54 | 708 | 11,550 |
| `grok2-community` | AI model, RAIL and custom | Tier 2 | 51 | 226 | 2,937 |
| `h-research` | AI model, RAIL and custom | Tier 2 | 49 | 354 | 4,188 |
| `deepfloyd-if-license` | AI model, RAIL and custom | Tier 2 | 31 | 137 | 3,570 |
| `apple-amlr` | AI model, RAIL and custom | Tier 2 | 30 | 49,260 | 2,159,742 |
| `intel-research` | AI model, RAIL and custom | Tier 2 | 28 | 3,574 | 64,135 |
| `apple-ascl` | AI model, RAIL and custom | Tier 2 | 26 | 505 | 4,023 |
| `other` | Vague label | Decision needed | 29,995 | 10,969,074 | 200,770,919 |
| `unknown` | Vague label | Decision needed | 5,489 | 2,229,585 | 96,882,358 |
| `cc` | Vague label | Decision needed | 1,947 | 628,494 | 11,737,262 |
| `gpl` | Vague label | Decision needed | 1,196 | 263,931 | 1,860,267 |
| `bsd` | Vague label | Decision needed | 478 | 102,159 | 2,423,891 |
| `lgpl` | Vague label | Decision needed | 50 | 1,047 | 19,739 |

The families are a first pass for review, not a legal classification; for example `ofl-1.1` is a font license and `afl-3.0` is academic, and both sit under permissive software here. Dataset counts include datasets that list more than one license.

## Caveats

The list of 83 licenses describes what authors typed into dataset metadata, and that limits what it can support.

- **Declared, not verified.** Nobody checks that a dataset's license tag matches the license text in its repository, so a tag can be wrong or out of date.
- **Most datasets say nothing.** 705,237 datasets (65%) declare no license, so an annotated license list covers a minority of the Hub whatever we do.
- **Hub identifiers are not SPDX identifiers.** Some Hub values are families or custom licenses (`openrail`, `llama3.1`, `other`), and a few need a judgment call before they map to one license text.
- **Snapshot in time.** The crawl reflects the Hub on 5 October 2026, and new licenses and datasets appear daily. The 30-day download counts move week to week.
- **Families and tiers are ours.** They are an organising aid for review, not a legal classification.

## Proposed next steps

The licenses are ordered below by usage, so that the gold-standard annotation covers the most-used ones first. Input is needed on the order and on items 3 and 4.

1. **Tier 1: 15 licenses.** `apache-2.0`, `mit`, `cc-by-4.0`, `cc-by-nc-4.0`, `cc-by-sa-4.0`, `openrail`, `cc0-1.0`, `cc-by-nc-sa-4.0`, `odbl`, `odc-by`, `cc-by-nc-nd-4.0`, `afl-3.0`, `creativeml-openrail-m`, `cc-by-sa-3.0`, `gfdl`. Together they cover 95% of the datasets that declare a specific license and 96% of those licenses' all-time downloads. `gfdl` and `cc-by-sa-3.0` are here because of their downloads, not their dataset counts.
2. **Tier 2: 62 licenses.** Annotated by family in this order: Creative Commons (9), open data and content (8), permissive software (13), copyleft and weak-copyleft software (14) and AI model, RAIL and custom (18). Each is under 0.5% of licensed datasets.
3. **AI model, RAIL and custom licenses (20, two of them in Tier 1).** These carry use restrictions that may be hard to express as ODRL rules. Decision needed: are they in scope for a dataset policy vocabulary?
4. **Vague labels and unlicensed datasets.** Decision needed: leave `other`, `unknown`, `cc`, `gpl`, `bsd` and `lgpl` unannotated, or resolve them per dataset from the card text. Datasets with no license get no policy.

In parallel, we will analyze which licenses co-occur in the multi-license datasets and sort them into alternative and cumulative cases, to seed the nested and dual-license ground truth.
