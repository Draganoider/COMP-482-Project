# GitHub Copilot — instructions

All project rules for AI agents live in [`AGENTS.md`](../AGENTS.md) at the repository root. Read it
and follow it. This file is a pointer, not a copy: add rules to `AGENTS.md`, never here.

The rules most often broken:

- Never invent, round or estimate a measured number. If it wasn't run, say so.
- Every algorithm is cross-checked against a brute-force implementation on small inputs.
- Pull requests go into `test`, not `main`.
- No AI attribution lines in commits or pull requests.
