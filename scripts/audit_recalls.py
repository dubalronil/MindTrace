"""Classify each REC_WORD event as a correct first recall, a repeat, or an intrusion."""

import csv

PATH = "data/raw/sub-LTP063_ses-0_task-ltpFR_beh.tsv"

with open(PATH) as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

presented = {}  # trial -> set of item_num presented
recalls = {}    # trial -> REC_WORD events in recall order
for r in rows:
    try:
        trial = int(r["trial"])
    except ValueError:
        continue
    if trial <= 0:
        continue
    if r["trial_type"] == "WORD":
        presented.setdefault(trial, set()).add(r["item_num"])
    elif r["trial_type"] == "REC_WORD":
        recalls.setdefault(trial, []).append(r)

correct = repeats = intrusions = 0
flagged = []
for trial in sorted(recalls):
    studied = presented.get(trial, set())
    seen = set()
    for r in recalls[trial]:
        item_num, item_name = r["item_num"], r["item_name"]
        if item_num not in studied:
            intrusions += 1
            flagged.append((trial, item_name, item_num, "intrusion"))
        elif item_num in seen:
            repeats += 1
            flagged.append((trial, item_name, item_num, "repeat"))
        else:
            correct += 1
            seen.add(item_num)

print(f"Correct first recalls: {correct}")
print(f"Repeated recalls:      {repeats}")
print(f"Intrusions:            {intrusions}")
print(f"Total REC_WORD events: {correct + repeats + intrusions}")

print("\nFlagged events (trial | item_name | item_num | type)")
if not flagged:
    print("  none")
for trial, item_name, item_num, kind in flagged:
    print(f"  {trial} | {item_name} | {item_num} | {kind}")
