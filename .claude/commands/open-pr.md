---
description: Push the current branch and open a pull request into test
---

Open a pull request for the current branch:

1. Refuse if the current branch is `test` or `main`: work belongs on its own branch.
2. Run the checks in `/check`. If any fails, stop and report; don't open the pull request.
3. Show me `git status` and `git diff` for anything uncommitted, and confirm the commit message
   before committing. No AI attribution lines.
4. Check that `CHANGELOG.md` has a line under *Unreleased* for this change, ending with the
   author's GitHub handle, and that any experiment's result is in `docs/llm-wiki/findings.md`.
   Ask me if either is missing.
5. Push the branch, then `gh pr create --base test`, filling in the repository's pull request
   template from the real changes. Ask me for the *Contribution* lines rather than guessing who did
   what. Extra context for the description: $ARGUMENTS
6. Print the pull request URL and remind me that a teammate reviews it before it merges.
