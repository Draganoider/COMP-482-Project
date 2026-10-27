# LLM Wiki

Working knowledge for whoever touches this repo next, human or AI. It exists because the project
depends on facts that are expensive to rediscover: what a benchmark measured and under which
conditions, how the course wants a proof written, why a setup step fails on Windows. Write a fact
down once and nobody has to re-derive it, and no AI assistant has to guess it.

## Where things live

| Question | Where |
|---|---|
| What are we doing, by when, and what was decided? | [../plan.md](../plan.md) |
| What did we measure, and under which conditions? | [findings.md](findings.md) |
| How do we time and compare algorithms fairly? | [benchmarking.md](benchmarking.md) |
| How does the course want pseudocode, proofs and runtime analysis written? | [course-conventions.md](course-conventions.md) |
| How do I set up my machine? | [environment.md](environment.md) |

The plan is the authority on scope and decisions. This wiki is for facts and measurements. Add a
row above for every new page: a page nobody can find is a page nobody reads.

## What goes where

| Kind of knowledge | Where |
|---|---|
| Rules every session must follow, and lessons | [AGENTS.md](../../AGENTS.md) |
| What changed, and when | [CHANGELOG.md](../../CHANGELOG.md) |
| Phases, scope, roles, decisions and open questions | [plan.md](../plan.md) |
| How something works, in depth; setup; measurements | here, one topic per page |

The plan says what we're building and why; a page here says how it works. When a plan section
grows into the second, move it here and leave a link.

## The rule that matters most

**A number without its conditions isn't a result.** Every measurement needs the machine, the input
sizes, the seed, the number of repetitions and the commit next to it. Timings change with all of
them, and a number that can't be repeated can't go in the report.

## How to write here

1. **Same day.** Record a result or a surprising fact the day you learn it.
2. **In the same pull request.** A page that describes code or an experiment changes in the pull
   request that changes them. A wrong page is worse than none, because it is believed.
3. **Facts carry a date and a version.** "Python 3.12's `heapq` ... (checked 2026-11-02)" stays
   useful; an undated claim silently goes stale.
4. **Correct in place.** When a recorded fact turns out wrong, fix it and note what changed.
5. **Negative results are the most valuable entries.** "The heap was slower than the array up to
   V = 2,000" saves more time than "the heap worked".
6. **Link the source** for anything taken from documentation or a paper.
7. **Distilled, not narrated.** Facts and reasons, in tables where they fit.
