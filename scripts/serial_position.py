"""Serial-position recall probabilities for one PEERS ltpFR session."""

import csv
import sys

if len(sys.argv) != 2:
    sys.exit("usage: python3 scripts/serial_position.py <behavioral.tsv>")

PATH = sys.argv[1]
LIST_LENGTH = 16

with open(PATH) as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

presented = {}  # trial -> item_num in presentation order
recalled = {}   # trial -> set of item_num recalled that trial
for r in rows:
    try:
        trial = int(r["trial"])
    except ValueError:
        continue
    if trial <= 0:
        continue
    if r["trial_type"] == "WORD":
        presented.setdefault(trial, []).append(r["item_num"])
    elif r["trial_type"] == "REC_WORD":
        recalled.setdefault(trial, set()).add(r["item_num"])

hits = [0] * LIST_LENGTH
totals = [0] * LIST_LENGTH
for trial, items in presented.items():
    recalled_here = recalled.get(trial, set())
    for position, item_num in enumerate(items):
        totals[position] += 1
        if item_num in recalled_here:
            hits[position] += 1

print("Position | Recalled | Total | Recall Probability")
for position in range(LIST_LENGTH):
    n, total = hits[position], totals[position]
    print(f"{position + 1} | {n} | {total} | {n / total:.3f}")

print(f"\nPresented studied items: {sum(totals)}")
print(f"Recalled studied items:  {sum(hits)}")
print(f"Overall recall probability: {sum(hits) / sum(totals):.3f}")
