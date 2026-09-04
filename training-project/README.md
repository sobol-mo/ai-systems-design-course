# AI Engineering training project

Status: Laboratory 01 workstation doctor and governed-proposal workflow implemented.

This directory holds the neutral cumulative AI system built across the eight laboratories. It runs
without access to the instructor's private repositories or personal data: every artefact you produce
here is your own.

The clone that contains this directory is one Git repository. `origin` is the student's GitHub fork.
`upstream` is https://github.com/sobol-mo/ai-systems-design-course. Folders are not remotes.
Upstream-owned paths may be overwritten by a later instructor publication. Student work is committed
only under `student/` and `reports/` and is pushed only to `origin`.

```text
training-project/
  README.md, pyproject.toml, uv.lock, .gitignore   upstream
  boundary-proposal.yaml                           upstream starter — copy into reports/lab01/
  fixtures/                                        upstream
  platform/                                        upstream
  tests/public/                                    upstream
  student/                                         student-owned — create, commit, push to origin
  reports/                                         student-owned — create, commit, push to origin
  .venv/                                           derived — never commit
```

## What exists now

Laboratory 01 contributes the governed-proposal workflow. It encodes one rule of the course: an AI
model may propose, but only a recorded human decision may accept. The workflow refuses to apply a
proposal that no human explicitly approved, and it refuses to overwrite a decision that was already
recorded. The decision contains a SHA-256 digest of the reviewed proposal, so changing proposal
content after the decision invalidates approval. Reapplying unchanged approved content is idempotent.

The `doctor` command writes a normalized machine-readable report for a supported Windows or Linux host
and the Git, GitHub CLI, `uv`, and Obsidian capabilities. Authenticated Antigravity CLI is recorded when
present; it is not required for a green report when another agent subscription is used.

Three files carry the protocol, and each has exactly one owner:

| File | Written by | Meaning |
|---|---|---|
| `reports/lab01/boundary-proposal.yaml` | the AI, edited by you | a candidate system boundary, with no authority |
| `reports/lab01/boundary-decision.json` | the `decide` command | the recorded human decision, the only authority |
| `student/design/learning-system-boundary.yaml` | the `apply` command | the accepted contract, never edited by hand |

## Running it

```bash
uv sync
uv run learning-project doctor --output reports/lab01/environment-report.json
uv run learning-project validate reports/lab01/boundary-proposal.yaml
uv run learning-project decide reports/lab01/boundary-proposal.yaml --approve --by "your-name" --decision reports/lab01/boundary-decision.json
uv run learning-project apply reports/lab01/boundary-proposal.yaml --decision reports/lab01/boundary-decision.json --output student/design/learning-system-boundary.yaml
```

`validate` changes nothing and reports every problem it finds. `decide` records your approval or
rejection, with `--reject --reason "..."` for a rejection. `apply` writes the accepted contract, and
fails if the decision is missing, pending, rejected, or points at a different proposal.
Laboratory 01 creates the report and student-design directories and copies the starter proposal into
the report directory before these commands are used. The
command-line defaults place all three files beside the proposal; the explicit paths above preserve
the course ownership boundary instead.

## Running the tests

```bash
uv run python -m unittest discover -s tests/public -v
```

The tests under `tests/public/` are the specification of the workflow. Read them before you change
the code: they state what the protocol must guarantee, not how it is implemented.

## Later laboratories

The sample domain, data set, and supported local and API model options are introduced by the
laboratories that need them. Nothing outside `tests/public/` is a fixed interface yet.
