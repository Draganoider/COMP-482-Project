# Contributing

The short version, for the five of us. [AGENTS.md](AGENTS.md) has the full rules for humans and AI
assistants alike, and is worth reading once.

## Claiming work

- Every task is an issue. Pick one nobody is assigned to, **assign yourself**, and say so in the
  team chat. If you want one someone else has, ask them first.
- Check what it's **blocked by** before you start.
- Stick to the files the issue owns. That's what keeps five people from editing the same lines.
- Filing something new? Use the **Task**, **Bug**, **Experiment result** or **Assignment question**
  form.

## Making a change

```bash
git switch test && git pull
git switch -c feature/short-name
```

Commit, push, and open the pull request **into `test`**, the default branch: `gh pr create`. Fill
in the template honestly, including the *Contribution* section, with `Closes #N` only when the issue's
whole checklist is done, or `Part of #N` otherwise.

- One teammate reviews it before it merges, following [REVIEWING.md](REVIEWING.md).
- **Small fixes** (a typo, a broken link, a doc correction, a one-liner that doesn't change what an
  algorithm computes or an experiment measures) may be committed straight to `test`.
- `main` is protected: only a reviewed pull request from `test` gets in, when we submit a phase.
- Add a line to [CHANGELOG.md](CHANGELOG.md) under *Unreleased* for anything notable, ending with
  your GitHub handle.
- No `Co-Authored-By` or "Generated with" lines for AI tools. A `Co-authored-by:` for a teammate you
  paired with is welcome.

## Recording results

Ran an experiment? Put the numbers and the conditions in
[docs/llm-wiki/findings.md](docs/llm-wiki/findings.md), or file an **Experiment result** issue and
copy it over. The report can only cite what's recorded.

## Where things are

| Path | What |
|---|---|
| [docs/plan.md](docs/plan.md) | Status, deadlines, roles, decisions, open questions |
| [docs/assignments/](docs/assignments/project-outline.md) | What the course asks for |
| [docs/llm-wiki/](docs/llm-wiki/README.md) | What we know and what we measured |
| [docs/proposal/](docs/proposal/README.md), [docs/report/](docs/report/README.md) | Drafts of the two submissions |
| [AGENTS.md](AGENTS.md) | The rules, for humans and AI assistants |
| [REVIEWING.md](REVIEWING.md) | How to review a pull request |
