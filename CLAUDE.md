@AGENTS.md

# Claude Code — project notes

The line above imports [AGENTS.md](AGENTS.md), which holds **all** the project rules and is shared
with every other AI agent used here (Codex, Cursor, Copilot and so on).

**Add project rules to AGENTS.md, not to this file.** Anything written only here is invisible to
every other agent, and the two files drift apart silently.

This file exists because Claude Code loads `CLAUDE.md` rather than `AGENTS.md`. Only
Claude-specific configuration notes belong below.

## Claude-specific configuration

Tool configuration lives in [.claude/](.claude/README.md):

- `.claude/settings.json` is committed and applies to the whole team. It sets `attribution.commit`
  and `attribution.pr` to empty strings, which is how hard rule 5 (no AI attribution lines) is
  enforced for Claude Code; other agents follow it by convention, and CI checks it.
- `.claude/settings.local.json` is for personal overrides, and is gitignored.
- Slash commands live in [.claude/commands/](.claude/commands/): `/start-feature`, `/check`,
  `/open-pr`.
