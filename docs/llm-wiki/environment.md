# Environment

Setting up a machine to work on the project. Language-specific steps are added once the language is
chosen (plan D4).

## Everyone

| Tool | Why | Check |
|---|---|---|
| Git | Version control | `git --version` |
| GitHub CLI | `gh pr create`, `gh pr checkout`, the review flow | `gh auth status` |
| Python 3.11 or newer | Everything we write (plan D8) | `python --version` |

```bash
gh repo clone Draganoider/COMP-482-Project
cd COMP-482-Project
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

`pip install -e` installs our package, `evac`, in editable mode: edits in `src/evac/` take effect
without reinstalling. Activate the virtual environment in every new terminal before running
`pytest`, `ruff` or an experiment. In VS Code, pick `.venv` as the interpreter
(*Python: Select Interpreter*) and the editor does it for you.

On Windows, if `Activate.ps1` is refused with "running scripts is disabled", run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once in PowerShell, or use
`.venv\Scripts\activate.bat` from cmd.

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
