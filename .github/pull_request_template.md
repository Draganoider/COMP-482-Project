<!--
Day-to-day work goes into `test`, the default branch. `main` is only for submissions.
Submitting a phase (test into main)? Use the submission template instead:
  gh pr create --base main --head test --template submission.md
-->

## What this changes

<!-- One or two sentences: what and why, not how. -->

## Issue

Closes #<!-- number -->

<!-- Write "Part of #N" instead if this doesn't finish every item in the issue's checklist, so merging doesn't close unfinished work. -->

## Contribution

<!-- Who did what, for the report's contributions section. One line per person, with their GitHub handle. -->

- @handle: 

## Checks

- [ ] This pull request goes into `test`
- [ ] Tests pass locally, and CI is green
- [ ] New or changed algorithms are cross-checked against a brute-force or reference implementation on small random inputs
- [ ] The code implements the pseudocode it claims to, with the data structure the analysis assumes, or the difference is written down
- [ ] Edge cases covered: empty input, one element, ties, and whatever else applies to this problem
- [ ] No secrets, no files over 2 MB, and no AI attribution lines in commits or this description
- [ ] External code or data is credited in `docs/references.md`
- [ ] A line under *Unreleased* in `CHANGELOG.md`, ending with the author's handle

## If this adds or changes an experiment

<!-- Delete this section if it doesn't. -->

- [ ] Runs with one command, listed in the README's *Running the experiments* table
- [ ] Fixed seeds; input generation is outside the timed region; repetitions with a median (`docs/llm-wiki/benchmarking.md`)
- [ ] Writes its CSV and plot to `results/`
- [ ] The result is recorded in `docs/llm-wiki/findings.md` with its conditions, and the numbers below match it

## Docs

- [ ] `docs/plan.md`, `AGENTS.md` (*Current state*) and the llm-wiki updated if this makes them untrue
- [ ] Any measurement or surprising fact recorded in `docs/llm-wiki/findings.md`, negative results included
- [ ] If this needs no changelog line, wiki update or finding, the reason is under *Notes for the reviewer*

## Notes for the reviewer

<!-- Anything you're unsure about, or want a second opinion on. -->

---

Reviewing this? [`REVIEWING.md`](https://github.com/Draganoider/COMP-482-Project/blob/test/REVIEWING.md) has the checks, in order, and the summary template.
