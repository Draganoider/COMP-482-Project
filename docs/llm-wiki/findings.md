# Findings

Measurements from running **this repository's code**, newest first. Every entry needs its
conditions (see [README.md](README.md)). File an **Experiment result** issue if that's easier, then
copy the result here. The report's results section is written from this page only.

**AI assistants:** never add a number you didn't get from a run, and never fill a table with
expected values (AGENTS.md hard rule 1).

---

## Hypotheses to test

What the analysis predicts and the experiments must confirm or refute. Filled in from the proposal's
evaluation plan. Whoever answers one moves it into a dated entry under Results.

| # | Hypothesis (from the analysis) | Experiment | Status |
|---|---|---|---|
| H1 | Edmonds-Karp's augmenting-path count stays within its O(VE) bound and its time within O(VE²); Ford-Fulkerson's depends on the flow value, so it can win when flows are small | E1 | Open |
| H2 | Closing a road lowers the max flow only if the road lies on some minimum cut | E2 | Open |
| H3 | Widening a min-cut road is not always the best single road to widen: with several minimum cuts it may change nothing, which brute force will show | E3 | Open |
| H4 | With no fire, the time-expanded result approaches layer 1's rate × time as the window grows; road closures and a later evacuation order push it lower | E4 | Open |
| H5 | The max-flow plan never gets fewer cars out than everyone taking their shortest route, and the gap is largest when one shelter is nearest to most households | E5 | Open |

---

## Entry format

```markdown
### <short title> (YYYY-MM-DD)

**Hypothesis:** H<n>, or what you set out to learn.
**Command:** the exact command from the README, with its arguments.
**Commit:** short hash. **Machine:** CPU, RAM, OS, language version. Plugged in, nothing else running?
**Inputs:** generator or dataset, sizes, seed(s), repetitions per size.
**Result:**

| n | Algorithm A (median ms) | Algorithm B (median ms) | Ops A | Ops B |
|---|---|---|---|---|

**Plot:** `results/<file>.png`
**What it shows:** one or two sentences. Does it confirm the hypothesis? Where does it not?
**Caveats:** anything that limits it (small sizes, noisy machine, one seed).
```

---

## Results

*None yet.*
