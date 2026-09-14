"""Audit a PEERS ltpFR behavioral file: WORD and REC_WORD counts per trial."""

import csv

PATH = "data/raw/sub-LTP063_ses-0_task-ltpFR_beh.tsv"

with open(PATH) as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

trial_types = sorted({r["trial_type"] for r in rows})

counts = {}
for r in rows:
    try:
        trial = int(r["trial"])
    except ValueError:
        continue
    if trial <= 0:
        continue
    presented, recalled = counts.setdefault(trial, [0, 0])
    if r["trial_type"] == "WORD":
        counts[trial][0] = presented + 1
    elif r["trial_type"] == "REC_WORD":
        counts[trial][1] = recalled + 1

print(f"{'trial':>5}  {'WORD':>5}  {'REC_WORD':>8}")
for trial in sorted(counts):
    presented, recalled = counts[trial]
    print(f"{trial:>5}  {presented:>5}  {recalled:>8}")

print(f"\nPositive trial numbers: {len(counts)}")
print(f"Unique trial_type values ({len(trial_types)}):")
for t in trial_types:
    print(f"  {t}")
