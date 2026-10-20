# Environment

Setting up a machine to work on the project. Language-specific steps are added once the language is
chosen (plan D4).

## Everyone

| Tool | Why | Check |
|---|---|---|
| Git | Version control | `git --version` |
| GitHub CLI | `gh pr create --base test`, `gh pr checkout`, the review flow | `gh auth status` |
| Python 3 | Runs `.github/scripts/check_links.py`, whatever the project language | `python --version` |

```bash
gh repo clone Draganoider/COMP-482-Project
cd COMP-482-Project
python .github/scripts/check_links.py
```

## Line endings

`.gitattributes` makes every text file LF in the repository, whatever your OS, and `.editorconfig`
tells editors to match. Nothing to configure. If Git warns that "LF will be replaced by CRLF",
that's your local `core.autocrlf` and it's harmless.

## AI assistants

[AGENTS.md](../../AGENTS.md) is read by Codex, Cursor, Gemini CLI and others directly; Claude Code
reads it through [CLAUDE.md](../../CLAUDE.md), and Copilot through
[.github/copilot-instructions.md](../../.github/copilot-instructions.md). Shared Claude Code
settings and slash commands are in [.claude/](../../.claude/README.md).

## Known problems

*None yet. Add them here, dated, with the fix.*
