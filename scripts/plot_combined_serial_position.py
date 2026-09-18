"""Plot the serial-position curve pooled across PEERS ltpFR sessions.

Same scoring logic as scripts/combine_serial_position.py. Trials are keyed by
(file, trial) because trial numbers restart in every session.
"""

import csv
import os
import re
import sys

import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    sys.exit("usage: python3 scripts/plot_combined_serial_position.py <behavioral.tsv> [...]")

PATHS = sys.argv[1:]
LIST_LENGTH = 16

subjects, sessions = [], []
for path in PATHS:
    name = os.path.basename(path)
    match = re.search(r"sub-([^_]+)_ses-(\d+)", name)
    if not match:
        sys.exit(f"cannot read subject/session from filename: {name}")
    subjects.append(match.group(1))
    sessions.append(int(match.group(2)))

if len(set(subjects)) > 1:
    sys.exit(f"files span more than one subject: {sorted(set(subjects))}")
SUBJECT = subjects[0]
FIRST, LAST = min(sessions), max(sessions)

if FIRST == LAST:
    TITLE = f"Serial Position Curve — {SUBJECT}, Session {FIRST}"
    OUT = f"results/figures/serial_position_{SUBJECT}_combined_ses{FIRST}.png"
else:
    TITLE = f"Serial Position Curve — {SUBJECT}, Sessions {FIRST}–{LAST}"
    OUT = f"results/figures/serial_position_{SUBJECT}_combined_ses{FIRST}-{LAST}.png"

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

positions = list(range(1, LIST_LENGTH + 1))
probabilities = [n / total for n, total in zip(hits, totals)]
for position, p in zip(positions, probabilities):
    print(f"{position} | {p:.3f}")

print(f"\nFiles analyzed:  {len(PATHS)}")
print(f"Trials analyzed: {len(presented)}")
print(f"Presented studied items: {sum(totals)}")
print(f"Recalled studied items:  {sum(hits)}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(positions, probabilities, marker="o", linewidth=2, markersize=6)
ax.set_xlabel("Serial Position")
ax.set_ylabel("Recall Probability")
ax.set_ylim(0, 1)
ax.set_xticks(positions)
ax.set_title(TITLE)
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.tight_layout()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=150)
print(f"\nSaved {OUT}")
plt.show()
