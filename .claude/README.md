# `.claude/` — Claude Code configuration

Everything in here is project-scoped and shared by the team. Claude Code reads it automatically
when a session starts in this repository.

| Path | Committed | Purpose |
|---|---|---|
| `settings.json` | yes | Attribution off, `.env` and keys unreadable, read-only git and `gh` commands pre-approved |
| `settings.local.json` | **no** (gitignored) | Your personal overrides |
| `commands/` | yes | Slash commands: `/start-feature`, `/check`, `/open-pr` |

Settings load in the order **user → project → local**, so `settings.local.json` overrides
`settings.json`, which overrides your personal `~/.claude/settings.json`.

## Where the rules actually live

Not here, and not in `CLAUDE.md` either. **[AGENTS.md](../AGENTS.md) is the single source of
truth** for every AI agent. [CLAUDE.md](../CLAUDE.md) imports it with its first line, `@AGENTS.md`.

| Layer | File | Holds |
|---|---|---|
| Rules | `AGENTS.md` | Everything an agent must know or do. **Edit this one** |
| Adapter | `CLAUDE.md` | The `@AGENTS.md` import, plus Claude-only notes |
| Configuration | `.claude/settings.json` | How the tool behaves, not what it should do |

## Commands

| Command | Does |
|---|---|
| `/start-feature <what>` | Branches off the latest `test` with the right prefix, and plans before editing |
| `/check` | Runs what CI runs, and fixes what fails |
| `/open-pr <context>` | Checks, commits after you confirm, pushes, and opens a pull request into `test` |
