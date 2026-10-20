---
description: Run the same checks that CI runs
---

Run the checks CI will run, and fix what fails:

1. `python .github/scripts/check_links.py`
2. `git ls-files` contains nothing from `.scratch/`, `data/raw/` or `.env`, and no file over 2 MB.

The language's build, tests and lint are added here when the language is chosen (docs/plan.md, D4).

Report the real result. If something fails and you can't fix it confidently, show the failing
output and say what you think is wrong rather than guessing.
