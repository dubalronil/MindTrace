# MindTrace

MindTrace explores similarities and differences between human memory and memory behavior in AI systems.

## Research Question

**Do language models remember information in ways that resemble human memory?**

We begin with human free-recall data from the Penn Electrophysiology of Encoding and Retrieval Study (PEERS), where participants study word lists and later try to recall them.

## Dataset

We use the **PEERS** dataset, available publicly through OpenNeuro as **ds004395**.

[Open PEERS on OpenNeuro](https://openneuro.org/datasets/ds004395)

A browsable mirror is also available on NEMAR. The dataset includes behavioral (`BEH`) and EEG data; MindTrace currently uses only the behavioral files. :contentReference[oaicite:0]{index=0}

## Current Progress

- inspect individual recall trials
- summarize sessions
- identify correct recalls, repeats, and intrusions
- calculate serial-position recall probabilities

Current analysis is limited to one participant and one session.

## Next Steps

- plot the serial-position curve
- analyze more human data
- run comparable recall experiments with language models
- compare human and AI memory patterns
