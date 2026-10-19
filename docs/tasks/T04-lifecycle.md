# T04 — Complete lifecycle and recovery

Status: ready. Depends on: T02 + T03 (done). Executor: neutral tool agent.
Read [handoff](README.md), technical-plan sections 3–4, T03 evidence and
[ADR 0001](../decisions/0001-selective-guidance-reading.md).
T03's [acceptance and next-agent order](T03-acceptance.md) govern the connection;
do not resume superseded feasibility queues. T04 is ready, not implemented.

## Goal

Implement complete install/update/restore/status/verify/remove operations using
the tested native mechanisms, without a consumer-owned wrapper or probe.

## Work

- One operation performs preparation, connection and verification. Preview may be
  available but is not a mandatory separate configure/install sequence. Applying
  a retained proposal never re-resolves source tips.
- Persist confirmed bundle/client/scope selection. Routine updates preserve local
  exceptions and lint choices, and do not reinstall a compatible executable.
- Inventory only selected clients; preserve local instruction authority, user
  configuration/comments and unrelated guards. Detect competing legacy loaders.
- Track owned files/blocks, before/after bytes and a durable transaction journal;
  recheck preimages, publish activation last and retain working selections.
- Recover interrupted operations without overwriting unknown edits. Multi-file
  changes are not an atomic transaction merely because each file uses rename.
- Remove only owned integration; preserve unrelated edits and recorded selections.
  Modified owned material needs explicit resolution. No silent cache deletion.
- Verification is offline comparison against retained expected identity, not an
  implicit repair, source refresh or policy rebaseline.
- Connect the T03-accepted short-entry route for root-started work; leave topic
  relevance/dependencies authored beside the content. Do not add a selector engine,
  mandatory per-patch reads, all-topic injection or behavioral enforcement to `verify`.
- Keep strict integrity/ownership checks separate from observed client delivery,
  voluntary topic reads and application. Host success cannot certify model compliance.
- Report restart/reload needs. No live snapshot rewrite or hot-context guarantees.

## Accepted connection prerequisites from T03

- Start at the project/selected-worktree root, not a subdirectory. Retain/check the
  root identity separately from environment strings; `cwd` and `PWD` must agree.
- Claude imports the short index natively. Preserve existing root/folder policies;
  never bypass host-managed permissions or fabricate external-import approval.
- OpenCode V2 uses native `instructions`. The tested managed-host route keeps
  `OPENCODE_DISABLE_PROJECT_CONFIG=1` and supplies a host-controlled read-only
  `OPENCODE_CONFIG` with `instructions: ["{env:PWD}/AGENTS.md"]`. A fixed parent path
  fails worktree isolation; stale/missing `PWD` can silently select the wrong index.
- Define owned registration/merge/rollback and report operator prerequisites when
  host configuration is not writable or not authorized. Do not change live managed
  settings, add consumer launchers or broaden access as an implicit install step.
- Native entry arrival, selected-topic behavior and guard enforcement are different
  checks. No terminal-protection claim follows from a run that never offered that
  tool. Consumer guard verification and authorized activation remain separate.

## Acceptance

`unittest` covers complete lifecycle, no-ops, concurrent preparation, faults at
every write/publication stage, restart/retry, altered owned blocks, unrelated user
edits, changed content updates, retained-version recovery and exact restores.
Check engine/schema mismatches, root/scoped registration and source/link integrity.
Prove preservation of user bytes, not only equivalent parsed settings.

Run distribution/clean-install checks and macOS/Linux tests for supported behavior.
Repeat installed-client checks when the implementation changes T03's mechanism.
Confirm the installed root entry supports relevant topic reads and reuse under
T03's accepted limits, without duplicating folder/root delivery. Do not require a
monitoring service or ongoing read audit to install or use the package.
Measure every required setup/update/restore/removal step, including initial Python/
Git/tool acquisition. A wrapper hiding many required configurations is not success.

## Handoff

Record one documented usage path and tested commands. Mark T06 ready only after
T05 also passes. Do not migrate existing consumers in this task.
Keep [T08 observation](T08-lightweight-observation.md) out of lifecycle dependencies;
record instrumentation gaps rather than implementing unapproved capture machinery.
Completion evidence: pending.
