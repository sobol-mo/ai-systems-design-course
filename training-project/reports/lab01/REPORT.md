# Laboratory 01 Report

## Summary

Repository: `https://github.com/exideys/ai-systems-design-course.git`

Branch: `lab01/exideys`

Course commit used for source registration: `e4fb5c6bbb2cb150c6000ed1406dff10b6854690`

External Markdown vault: `C:\Users\lstar\OneDrive\ai-systems-learning-vault`, external to the course Git repository.

Proposer path: OpenAI Codex was used as the existing AI-agent interaction environment for the proposal step. Antigravity CLI was not used; `agy` was unavailable in PATH on 2026-09-17. The AI proposer edited only `reports/lab01/boundary-proposal.yaml`. The later `decide` and `apply` commands are deterministic project workflow commands and are recorded separately.

## Fixed System Boundary

The fixed system is the course-provided workstation-local AI-assisted learning knowledge system for technical concepts. The accepted boundary keeps the student-owned Markdown vault as canonical learning state outside the Git repository, keeps project definitions and evidence under Git, and treats runtime artifacts such as `.venv`, indexes, caches, or future graph views as rebuildable derived state.

The selected `personal_domain` is `Software engineering study notes for backend application design`. This is only a possible later bounded extension. It does not redefine the project as a backend-design product, does not authorize private-data ingestion, and remains subject to the same source, proposal, validation, human decision, and application workflow.

## Usefulness, Baseline, And Tradeoff

AI is useful here because it can draft a bounded proposal and expose uncertainty from the supplied theory and contracts faster than a fully manual draft. It still cannot approve its own output or prove that the proposal is semantically good. The simpler non-AI baseline is a manual Markdown checklist containing the source path, commit hash, semantic-review answers, and a human-written boundary summary. That baseline can already preserve provenance and support review, but it is slower and provides less assistance in spotting missing rationale.

The main tradeoff is between speed of proposal drafting and the risk of accepting fluent but weakly grounded text. The chosen boundary allows AI assistance only at the proposal stage, then requires deterministic validation and explicit student approval before accepted state is created.

## Workstation And Evidence

Preflight result: green Windows host. Observed values included Windows build `10.0.26200`, WinGet `v1.29.290`, Git `2.54.0.windows.1`, GitHub CLI package `2.101.0`, WinGet-installed `uv 0.12.15`, and Obsidian `1.13.7`.

The WinGet workstation configuration was applied twice and `provision.log` recorded both runs. The second run completed without intentional package changes outside the declared four packages. `environment-report.json` reports green Windows host capabilities for Git, GitHub CLI, `uv`, and Obsidian; `agy` is recorded as unavailable, which is acceptable because a different existing AI-agent environment was used.

`uv sync` created `.venv` as derived state. Targeted Lab01 public tests passed with `18` tests OK. A full `unittest discover -s tests/public -v` in this published tree also discovers Lab02 tests even though only Module 01 is present in `modules/`; those Lab02 tests fail for missing Module 02 materials and are not caused by the Lab01 artifacts.

Premature `apply` before a decision failed with a missing-decision error and did not create `student/design/learning-system-boundary.yaml`.

## Semantic Review Before Decision

1. The proposal preserves the supplied learning knowledge system and uses `personal_domain` only as a later bounded extension. Conclusion: approve.

2. The intended outcome names an observable student capability: tracing a concept to source evidence, explaining the accepted boundary, and justifying approval. It is not merely "use AI". Conclusion: approve.

3. The non-goals exclude private/sensitive data, high-consequence decisions, concept records, graph/vector indexes, and production architecture in Lab01. Conclusion: approve.

4. The governance fields keep AI at proposal authority, deterministic code at structural validation and digest-bound application, and the student at semantic approval. Because Codex was used as proposer, the report distinguishes the proposal edit from the later decision/apply workflow. Conclusion: approve.

5. The usefulness condition can be checked against preserved artifacts: source registration, proposal, decision, accepted contract, and review answers. Conclusion: approve.

6. The material risk is plausible: a fluent proposal could pass schema validation while being semantically weak, causing later work to rely on a bad boundary. Conclusion: approve.

7. The non-AI baseline is simpler and can preserve provenance and a manual boundary summary without AI. Conclusion: approve.

8. Required evidence covers deterministic behavior and semantic/source-grounded review: tests, doctor, validation, refused premature apply, decision, applied contract, and report answers. Conclusion: approve.

9. The uncertainty is real and bounded: later modules may refine schemas, relation vocabulary, and recovery expectations. Conclusion: approve.

Overall semantic-review conclusion: the candidate is acceptable for an approval decision.

## Recovery Explanation

The reproducible workstation environment is recovered by applying the controlled WinGet configuration and rechecking capabilities. The project artifacts under Git are recovered by cloning the student fork at the submitted commit and branch. The external Markdown vault is mutable canonical state and is not recovered from Git; it currently resides under OneDrive, giving an initial off-device synchronization measure. This is not a complete disaster-recovery design because unwanted changes can also sync, but it satisfies the Lab01 initial protection expectation.

## Why Validation Is Not Semantic Approval

`learning-project validate` checks structure: required fields, status, and schema-level invariants. It does not know whether the boundary is a good system design, whether evidence is sufficient, or whether the tradeoff is wise. That is why the semantic review and explicit decision are separate from validation.

## Control Questions

1. Evidence such as source provenance, proposal, semantic review, decision, digest-bound application, tests, and environment report distinguishes an engineered workflow from a model demo.

2. `boundary-proposal.yaml` is only a candidate. It becomes accepted only after a separate approved decision and `apply`.

3. AI may propose; the deterministic workflow may validate and apply an approved exact proposal; the student approves or rejects. CLI enforces schema, digest binding, and apply refusal, while role separation is also demonstrated by evidence.

4. A rejected decision is bound audit evidence. Editing it into approval would destroy provenance, so a new proposal/review cycle is required.

5. A usefulness condition is informative when it is observable against evidence, not merely an impression that output looks good.

6. The non-AI baseline shows what value can be achieved without model risk and helps decide whether AI assistance is justified.

7. The second WinGet configuration run and capability checks demonstrate convergence, not just one successful installation.

8. Canonical artifacts include the external Markdown vault records and accepted boundary. Audit evidence includes proposal, decision, report, environment report, and logs. Derived state includes `.venv`, caches, indexes, and rebuildable runtime outputs.

9. The vault stays outside Git because it is student-owned mutable canonical knowledge, not course project code. OneDrive synchronization is the current initial recovery mechanism.

10. The accepted tradeoff is faster AI-assisted drafting with human review instead of fully manual authoring. Evidence of weak grounding, privacy risk, cost, latency, or repeated review failures could trigger revision.

11. `origin` is the student fork and push target; `upstream` is the instructor course repository. Student commits are limited to `training-project/student/` and `training-project/reports/`.

12. Another agent subscription or manual fallback is allowed so the mandatory path does not require new paid access. The proposal file and deterministic gates remain `reports/lab01/boundary-proposal.yaml`, `validate`, `decide`, and `apply`.
