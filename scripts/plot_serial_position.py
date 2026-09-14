"""Plot the serial-position curve for one PEERS ltpFR session."""

import csv
import matplotlib.pyplot as plt

PATH = "data/raw/sub-LTP063_ses-0_task-ltpFR_beh.tsv"
OUT = "results/figures/serial_position_LTP063_ses0.png"
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

positions = list(range(1, LIST_LENGTH + 1))
probabilities = [n / total for n, total in zip(hits, totals)]
for position, p in zip(positions, probabilities):
    print(f"{position} | {p:.3f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(positions, probabilities, marker="o")
ax.set_xlabel("Serial Position")
ax.set_ylabel("Recall Probability")
ax.set_ylim(0, 1)
ax.set_xticks(positions)
ax.set_title("Serial Position Curve — LTP063, Session 0")
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print(f"\nSaved {OUT}")
plt.show()
