# T08 — Lightweight selective-reading observation

Status: pending. Depends on: T03 acceptance and an owner-authorized T06 clone pilot.
Executor: authorized client/consumer agent and reviewer; private access when needed.
Read [handoff](README.md), [ADR 0001](../decisions/0001-selective-guidance-reading.md)
and [T03's trial/limits](T03-selective-reading.md).

## Goal and scheduling

Learn whether agents consult sufficient relevant guidance without unnecessary
reading during representative work. Use existing client traces and manual review
first; this task does not implement a monitoring system or enforce read-before-edit.

T08 can start alongside the authorized T06 disposable-clone pilot, then sample
ordinary work only after separately authorized activation. It is not a dependency
of T04, T06 completion or T07 publication. Do not add an observation waiting period
or a statistical certification gate. Concrete failures affecting acceptance/support
claims must still be reported and resolved or explicitly limited by owner/reviewer.

## Inputs and boundaries

- A small, declared sample of tasks, retained guidance selection/policy identity,
  actual client/model versions, and owner-approved existing trace access.
- Explain the sampling window and task selection; include failures and unknowns,
  not just successful examples. No live task execution is authorized by this file.
- No delivery hooks, plugins, daemon, global telemetry, forced guide reads, per-project
  wrappers/probes, new engine command or automatic capture/upload/retention policy.
- Use only necessary trace excerpts. Preserve authorized originals privately;
  redact secrets and keep consumer prompts, source and classification evidence in
  the private owner's repository. Record missing access instead of broadening it.

## Work

1. Before inspecting the read sequence, declare expected relevant topics and explicit
   dependencies from the task and authored conditions. If the task evolves, append
   a reasoned expectation for that change; do not rewrite the baseline to fit reads.
2. Inspect actual successful content delivery/reads and relevant edits in order.
   Include native attachments, skill loads or command-based reads when evidenced;
   a path name, tool request or model claim alone is not a successful content read.
3. Record reuse of previously visible guidance. A later patch is not another required
   read opportunity. Treat rereads after context loss/content changes as justified
   when evidenced; do not call them redundant automatically.
4. Classify late/omitted required topics, unnecessary unrelated reads, avoidable
   repeats, appropriate reads/reuse and unknowns. Incomplete/truncated traces or
   uncertain applicability mean unknown, not proof of omission or irrelevance.
5. Review code/results separately for application of the guidance. Reading is not
   comprehension, correct code or successful security enforcement.
6. Summarize counts with their denominators and unknowns per client/model/sample.
   Evaluate topic/task or layer-transition opportunities, not number of patches.
   Do not infer a factory-wide percentage or causal guarantee from a small sample.

A minimal private record needs: task category, retained selection/client/model,
expected topics/dependencies, observed read/edit order, reuse/context-loss notes,
classification, result-review outcome, evidence reference and proposed action.
No new mandatory consumer file or schema is introduced.

## Acceptance and next decision

Deliver one bounded baseline review with sample selection, counts/unknowns,
representative failures and limitations. State whether to keep the simple entry,
clarify authored triggers/dependencies, run another small sample, or propose a
specific stronger candidate. Owner/reviewer decide sufficiency; none is auto-enabled.
This task can finish with a useful baseline; continuous observation is not required.

Prefer entry/content improvements before adding machinery. A stronger approach
needs its own approved scope, preserved rules and new retained trial identity.
Publish only sanitized aggregate outcomes and link the decision rationale; never
upload raw consumer traces to this public repository or a social post.

## Handoff

Record commands/access used, sample bounds, client versions, checks, missing
evidence and the reviewed next action. Keep rollout, repository publication and
external posting permissions separate. Completion evidence: pending; no monitoring
or consumer activation has been implemented by creating this task.
