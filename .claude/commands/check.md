---
description: Run the same checks that CI runs
---

Run the checks CI will run, and fix what fails:

1. `ruff check .` (use `ruff check --fix .` for the automatic fixes)
2. `pytest`
3. `python .github/scripts/check_links.py`
4. `git ls-files` contains nothing from `.scratch/`, `data/raw/` or `.env`, and no file over 2 MB.

If `pytest` or `ruff` isn't found, the package isn't installed: `pip install -e ".[dev]"` in the
project's virtual environment.

Report the real result. If something fails and you can't fix it confidently, show the failing
output and say what you think is wrong rather than guessing.
