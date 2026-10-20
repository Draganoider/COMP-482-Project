---
description: Start a new branch off the latest test branch
---

Start work on: $ARGUMENTS

1. Check `git status`. If there are uncommitted changes, stop and ask what to do with them.
2. `git switch test && git pull` so the branch starts from the latest `test`.
3. Create a branch named after the work, using the `feature/`, `fix/`, `exp/`, `docs/` or `chore/`
   prefix that fits, with a short kebab-case name.
4. If there's an issue for this work, read it and list the files it owns.
5. Confirm which branch we are on and give a short plan before changing any files.

Rules from AGENTS.md: never commit to `main`; commit straight to `test` only for a small fix; no AI
attribution lines in commits.
