# Reviewing a pull request

For everyone who reviews here, teammates and AI assistants alike. [AGENTS.md](AGENTS.md) and the
pull request template are the author's side of a pull request; this is the reviewer's. Every pull
request into `test` gets one teammate's review before it merges. Pull requests into `main` need an
approval too, and GitHub enforces that one.

A review answers two questions. For the author: **what has to change before this merges, and
why?** For the team: **what did the reviewer actually check?** CI answers neither. A green check
means the tests that exist pass. It doesn't mean the algorithm is correct, that the tests would
catch it if it weren't, or that the experiment measures what the report will say it measures.

## Check, in this order

The early steps are the cheapest, and they catch the most expensive problems. Start from the pull
request's branch:

```bash
gh pr checkout <number>
```

Without the GitHub CLI: `git fetch origin pull/<number>/head:pr-<number>`, then
`git switch pr-<number>`.

1. **Read the issue before the diff.** Note its checklist and the files it owns. You are checking
   the pull request against those, not against its own description.

2. **Check the base branch and the file list.** Day-to-day work goes into `test`, never `main`.
   Every changed file outside the issue's scope needs a reason in the description.

   ```bash
   git diff --stat origin/test...HEAD
   ```

3. **Run it.** Run the tests, and run any experiment the pull request adds or changes with the
   exact command from the README. Write down what you ran. **If you couldn't run it, say so in the
   review.** That includes an AI assistant without the toolchain.

4. **Check correctness against the algorithm, not the tests.**
   - Does the code implement the pseudocode it claims to, with the data structure the analysis
     assumes? A sorted list where the analysis says heap changes the runtime.
   - Edge cases: empty input, one element, ties, disconnected graphs, negative weights, duplicate
     keys, whatever applies.
   - Is there a brute-force or reference cross-check on small random inputs (hard rule 1)?

5. **Read the tests as if the code were wrong.** Would each test fail if the property its name
   promises broke? A test that only checks the output has the right type tests nothing. A
   cross-check that runs on three hand-picked inputs misses what a hundred random ones catch.

6. **Check the experiment, if there is one.**
   - One command, listed in the README, writing to `results/` (hard rule 2).
   - Fixed seed; input generation outside the timed region; repetitions with a median or similar,
     as in [benchmarking.md](docs/llm-wiki/benchmarking.md).
   - The input sizes are large enough, and spread widely enough, to show the growth rate.
   - The result is recorded in [findings.md](docs/llm-wiki/findings.md) with its conditions, and
     every number in the pull request description matches it.

7. **Check the paperwork.** The description matches the diff. `Closes #n` only when every
   checklist item is met; otherwise `Part of #n`. A changelog line with the author's handle, saying
   what changed and why. External code or data credited in [docs/references.md](docs/references.md).
   Every doc or llm-wiki page that describes what changed is updated in the same pull request; a
   stale page is a **Should fix**. No AI attribution lines in commits or the description.

A pull request that changes only docs skips steps 3 to 6; say so under *How I reviewed*.

## Label every finding

| Label | Use it for | The author |
|---|---|---|
| **Blocking** | Anything that must change before merge | fixes it, or changes your mind |
| **Should fix** | Worth doing in this pull request | fixes it, or opens an issue and links it |
| **Nit** | Taste, typos, small tidy-ups | may ignore it without replying |
| **Question** | Something you don't know | answers before merge; the answer may become any of the above |

**Blocking** is for: failing tests or CI; a wrong result on some input; code that doesn't match the
analysed algorithm; a claim with no evidence behind it; an experiment that can't be rerun with one
command; a secret or a large file in the diff; a checklist item missing with no reason given; or a
description that claims work the diff doesn't contain.

Write every finding as **where** (file and line), **what** is wrong, **why it matters**, and **a
fix** when you have one. Inline comments start with their label: `**Nit** — ...`. Comment on the
code, never the person.

## Write the summary

Paste this into the summary box under *Review changes*, or save it once as a
[saved reply](https://github.com/settings/replies). Delete any section that would be empty, except
*Verdict* and *How I reviewed*.

```markdown
**Verdict: <Approve | Changes requested | Needs a decision from @who>.** <The main reason, in one sentence.>

### What works
- <Specific: what should survive the rework, and why it is right.>

### Blocking
1. **<Short title>** — `<path>:<line>`
   <What is wrong.> <Why it matters.> <Suggested fix.>

### Should fix
1. **<Short title>** — `<path>:<line>`
   <What, why, fix.>

### Nits
- `<path>:<line>` — <one line each>

### Questions
- <What you need to know, and why the verdict depends on it.>

### Issue checklist (#<issue>)
| Item | Status | Note |
|---|---|---|
| <copied from the issue> | Done / Partly / Not done / Done differently | |

### How I reviewed
- Issue #<n> read. Changed files against the issue: <all in scope / list of others, all explained>
- Tests: <n passed, n failed>. Experiment: <ran `<command>`, results match findings.md / not run, because <reason>>
- Correctness: <edge cases tried, cross-check present / missing>
```

Then choose the matching GitHub state: *Approve*, *Request changes*, or *Comment* for a decision
someone else has to make.

Posting a review an AI assistant drafted makes it yours. Read it, and check its blocking claims,
before it goes out under your name.

## When the author pushes again

Review only what changed (*Files changed → Changes since your last review*). Resolve the threads you
opened once they're fixed, and update your verdict.

## Why these checks

- **Correctness against the algorithm.** The report's runtime analysis describes the pseudocode. If
  the code is a different algorithm, both the analysis and the experiment stop meaning anything.
- **Tests as if the code were wrong.** The brute-force cross-check is the strongest correctness
  evidence we have, and the cheapest to get wrong.
- **The experiment's method.** Timings are noisy. Without fixed seeds, repetitions and sizes that
  span orders of magnitude, a plot can show whatever you hoped for.
- **Saying what you didn't check.** A review is evidence. One that quietly skipped running the code
  tells the team it works when nobody knows.
