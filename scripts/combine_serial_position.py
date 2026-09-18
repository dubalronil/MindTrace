"""Serial-position recall probabilities pooled across PEERS ltpFR sessions.

Same scoring logic as scripts/serial_position.py, applied to several
behavioral TSVs at once. Trials are keyed by (file, trial) because trial
numbers restart in every session.
"""

import csv
import sys

if len(sys.argv) < 2:
    sys.exit("usage: python3 scripts/combine_serial_position.py <behavioral.tsv> [...]")

PATHS = sys.argv[1:]
LIST_LENGTH = 16

presented = {}  # (file, trial) -> item_num in presentation order
recalled = {}   # (file, trial) -> set of item_num recalled that trial
for path in PATHS:
    with open(path) as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    for r in rows:
        try:
            trial = int(r["trial"])
        except ValueError:
            continue
        if trial <= 0:
            continue
        key = (path, trial)
        if r["trial_type"] == "WORD":
            presented.setdefault(key, []).append(r["item_num"])
        elif r["trial_type"] == "REC_WORD":
            recalled.setdefault(key, set()).add(r["item_num"])

hits = [0] * LIST_LENGTH
totals = [0] * LIST_LENGTH
for key, items in presented.items():
    recalled_here = recalled.get(key, set())
    for position, item_num in enumerate(items):
        totals[position] += 1
        if item_num in recalled_here:
            hits[position] += 1

print("Position | Recalled | Total | Recall Probability")
for position in range(LIST_LENGTH):
    n, total = hits[position], totals[position]
    print(f"{position + 1} | {n} | {total} | {n / total:.3f}")

print(f"\nFiles analyzed:  {len(PATHS)}")
print(f"Trials analyzed: {len(presented)}")
print(f"Presented studied items: {sum(totals)}")
print(f"Recalled studied items:  {sum(hits)}")
print(f"Overall recall probability: {sum(hits) / sum(totals):.3f}")
