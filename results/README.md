# Results

What the experiments in [`experiments/`](../experiments/README.md) write: one folder per experiment
(`e1/`, `e2/`, ...), each with its CSV tables and the plots made from them.

- **Committed:** the results the report uses are evidence, so they stay in git, with the
  [findings.md](../docs/llm-wiki/findings.md) entry that records how they were made.
- **Not committed:** `results/tmp/` for trial runs, and anything over 2 MB (CI rejects it).
- **Never edited by hand.** A result changes only by rerunning its experiment.
