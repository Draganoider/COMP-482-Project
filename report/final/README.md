# Final report

8–12 pages, one PDF per team, submitted on Canvas with the repository link and the slides (if
any). The draft lives wherever the team writes together; link it here once it exists, and commit
the submitted PDF and slides to this folder.

- **Draft:** *link here*
- **Submitted PDF:** *added when submitted*

## Sections, owners and evidence

The structure the outline recommends. The Report Lead assigns owners; every section is reviewed by
someone who didn't write it.

| Section | Owner | Written from |
|---|---|---|
| Title page | | [../plan.md](../../docs/plan.md#team-and-roles) |
| Project contributions | | [../../CHANGELOG.md](../../CHANGELOG.md) (every line names its author), the pull requests' *Contribution* sections, `git shortlog -sn` |
| Introduction | | The proposal |
| Algorithm design / methodology | Algorithms Lead | Pseudocode and proofs; the code, which must match it (AGENTS.md hard rule 3) |
| Results and discussion | Experiments Lead | [../llm-wiki/findings.md](../../docs/llm-wiki/findings.md) only: every number and plot traces to an entry there and a file in `results/` |
| References | | [../references.md](../../docs/references.md) |

## Before submitting

- [ ] Every runtime claim has a matching experiment in `findings.md`, and the plot is in the report.
- [ ] Every number in the report appears in `findings.md` or a file in `results/`.
- [ ] Every experiment in the report runs with the one command the README lists, on a fresh clone.
- [ ] The pseudocode matches the code, or the differences are stated.
- [ ] Strengths and limitations are honest, including where an algorithm lost.
- [ ] Every external source in the report is in `references.md`, and the other way round.
- [ ] Page count is within 8–12.
