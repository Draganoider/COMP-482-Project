<!--
Submission pull request: `test` into `main`, once per phase.
Open it with: gh pr create --base main --head test --template submission.md
Merge with "Create a merge commit", never squash.
-->

## Submission

Phase: <!-- proposal / final -->

<!-- One or two sentences: what is being submitted. -->

## What's in it

<!-- Paste the Unreleased section of CHANGELOG.md here. -->

## Submission checklist

- [ ] This pull request goes from `test` into `main`
- [ ] CI is green on the latest `test` commit
- [ ] `CHANGELOG.md`: *Unreleased* renamed to `[<phase>] — YYYY-MM-DD`, with a new empty *Unreleased* above it
- [ ] `AGENTS.md` *Current state* and `docs/plan.md` status are up to date
- [ ] The submitted PDF (and slides, if any) are committed in `docs/proposal/` or `docs/report/`

### Final report only

- [ ] On a fresh clone, every experiment in the README runs with its one command and reproduces the numbers in `docs/llm-wiki/findings.md`
- [ ] Every number and plot in the report traces to `findings.md` and a file in `results/`
- [ ] The README explains setup, the tests and every experiment, and the *AI usage* section is filled in
- [ ] `docs/references.md` matches the report's references
- [ ] The report's contributions section agrees with `CHANGELOG.md` and the history

## After merging

- [ ] Tag the merge commit: `git switch main && git pull && git tag -a <phase> -m "<Phase> as submitted" && git push origin <phase>`
- [ ] GitHub Release for the tag, with the PDF attached: `gh release create <phase> --verify-tag --title "<Phase>" <pdf>`
- [ ] The Project Lead submits on Canvas, with the repository link
