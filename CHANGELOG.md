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

## [Unreleased]

### Changed

- **repo:** `test` is now the default branch, so `Closes #N` closes issues on merge into `test` and
  new pull requests target it; `main` stays protected as the release branch (plan D5). @Draganoider

### Added

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
