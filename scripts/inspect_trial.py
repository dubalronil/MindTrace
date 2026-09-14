"""Inspect one trial of a PEERS ltpFR behavioral file: presented vs. recalled words."""

import csv

PATH = "data/raw/sub-LTP063_ses-0_task-ltpFR_beh.tsv"
TRIAL = "1"

with open(PATH) as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if r["trial"] == TRIAL]

presented = [r["item_name"] for r in rows if r["trial_type"] == "WORD"]
recalled = [r["item_name"] for r in rows if r["trial_type"] == "REC_WORD"]

print(f"Trial {TRIAL}: {len(presented)} presented, {len(recalled)} recalled\n")

print("PRESENTED (serial position -> word)")
for i, word in enumerate(presented, start=1):
    print(f"  {i:2d}  {word}")

print("\nRECALLED (output position -> word -> serial position)")
for i, word in enumerate(recalled, start=1):
    pos = presented.index(word) + 1 if word in presented else None
    print(f"  {i:2d}  {word:<12} {pos if pos else 'INTRUSION (not in list)'}")
