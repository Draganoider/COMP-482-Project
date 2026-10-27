# Changelog

Every notable change to the project. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Instead of version numbers, sections are
named after the submissions: `proposal` and `final`.

How it's kept (see [AGENTS.md](AGENTS.md#working-conventions)):

- Every notable change adds a line under **Unreleased** in the same pull request, in one of these
  sections: Added, Changed, Fixed, Removed.
- Start the line with the area when it isn't obvious: **algorithms**, **tests**, **experiments**,
  **data**, **docs**, **report**, **repo**.
- **End the line with the author's GitHub handle** (several for pair work). The report's
  contributions section is written from this file.
- Submitting a phase (the `test` → `main` pull request) renames **Unreleased** to the phase and
  date, tags `main`, and starts a new empty **Unreleased**.

What is still to do is in the issue tracker and the [plan](docs/plan.md#status), not here.

## [Unreleased]

### Changed

- **docs:** `AGENTS.md` gains a *Where knowledge lives* table (plan, changelog, llm-wiki) and a
  *Lessons* section, and says a feature brings its own changelog line, wiki update and finding in
  its pull request; the PR template asks for the finding or a reason. The llm-wiki index says what
  goes where, the docs map lists the changelog, and the setup and benchmarking pages no longer wait
  for a language. The unlinked copy of `/check` in `.agents/skills/` is gone. @Draganoider
- **repo:** pull requests merge with a merge commit, so each branch stays visible in the history;
  squash and rebase merging are off. @Draganoider
- **docs:** the proposal and report checklists moved from `docs/` to `report/`; the topic
  comparison is now a dated snapshot in `docs/research/`. @Draganoider
- **repo:** `test` is now the default branch, so `Closes #N` closes issues on merge into `test` and
  new pull requests target it; `main` stays protected as the release branch (plan D5). @Draganoider

### Added

- **report:** a proposal skeleton in `report/proposal/skeleton.md`: each section with its owner,
  length and the points already agreed, for the Report and Presentation Lead to hand out.
  @Draganoider
- **repo:** the folders for each deliverable (`analysis/`, `src/evac/`, `tests/`, `experiments/`,
  `results/`, `data/`, `report/`, `app/`), each with a README saying what goes in it and who owns
  it; the Python package with `pyproject.toml`, pytest and ruff; a CI job that runs both; a test
  that fails if `src/` ever imports NetworkX. @Draganoider
- **docs:** the team's decisions (topic 6, three layers with the outline's baseline as the main
  deliverable, Python), the roles, the scope and experiments E1–E5 in `docs/plan.md`, and their
  hypotheses in `findings.md`. @Draganoider
- **docs:** the course's textbooks, syllabus order and proof style, checked against the lecture
  slides, in `course-conventions.md` and `references.md` (plan Q6 answered). Network flow is taught
  last, so a flow-based project learns it from the textbook first. @Draganoider
- **repo:** the repository and its conventions: `AGENTS.md` as the single rule file for people and
  AI agents, contributing and reviewing guides, pull request and issue templates, CI hygiene checks,
  `main` protected with `test` as the working branch, shared Claude Code settings and commands.
  @Draganoider
- **docs:** the plan, a summary of the project outline, the llm-wiki (benchmarking method, course
  conventions, findings), proposal and report checklists, and a comparison of the candidate topics
  from the implementation side. @Draganoider
